import json
from pyboy import PyBoy
from .api import get_chatgpt_response
from .component import connect_digit_list, read_prompt, read_prompt_without_template
from .index_data import *

fight_template = read_prompt("fight")
system_prompt = read_prompt_without_template("system_prompt")

class Fight:

    def __init__(self, pyboy_obj):
        self.lastfight = 1
        self.pyboy = pyboy_obj
        self.history = []
    
    def read_data(self):
        # return the data of game
        return {
            "enemy_id": self.pyboy.memory[0xCFE5],
            "enemy_type1": self.pyboy.memory[0xCFEA],
            "enemy_type2": self.pyboy.memory[0xCFEB],
            "enemy_move1": self.pyboy.memory[0xCFED],
            "enemy_move2": self.pyboy.memory[0xCFEE],
            "enemy_move3": self.pyboy.memory[0xCFEF],
            "enemy_move4": self.pyboy.memory[0xCFF0],
            "enemy_move_now": self.pyboy.memory[0xCFCC],
            "enemy_hp": connect_digit_list([self.pyboy.memory[0xCFE6],self.pyboy.memory[0xCFE7]]),
            "enemy_maxhp": connect_digit_list([self.pyboy.memory[0xCFF4],self.pyboy.memory[0xCFF5]]),
            "enemy_attack": connect_digit_list([self.pyboy.memory[0xCFF6],self.pyboy.memory[0xCFF7]]),
            "enemy_defense": connect_digit_list([self.pyboy.memory[0xCFF8],self.pyboy,memory[0xCFF9]]),
            "enemy_level": self.pyboy.memory[0xCFF0],
            "enemy_status": self.pyboy.memory[0xCFE9],

            "my_id": self.pyboy.memory[0xD014],
            "my_hp": connect_digit_list([self.pyboy.memory[0xD015],self.pyboy.memory[0xD016]]),
            "my_status": self.pyboy.memory[0xD018],
            "my_type1": self.pyboy.memory[0xD019],
            "my_type2": self.pyboy.memory[0xD01A],
            "my_move1": self.pyboy.memory[0xD01C],
            "my_move2": self.pyboy.memory[0xD01D],
            "my_move3": self.pyboy.memory[0xD01E],
            "my_move4": self.pyboy.memory[0xD01F],
            "my_maxhp": connect_digit_list([self.pyboy.memory[0xD023],self.pyboy.memory[0xD024]]),
            "my_attack": connect_digit_list([self.pyboy.memory[0xD025],self.pyboy.memory[0xD026]]),
            "my_defense": connect_digit_list([self.pyboy.memory[0xD027],self.pyboy.memory[0xD028]]),
            "my_level": self.pyboy.memory[0xD022],
            "my_move1_pp": self.pyboy.memory[0xD02D],
            "my_move1_pp": self.pyboy.memory[0xD02E],
            "my_move1_pp": self.pyboy.memory[0xD02F],
            "my_move1_pp": self.pyboy.memory[0xD030],

            "fight_mod": self.pyboy.memory[0xD057],
        }
    
    def dump_data(self, data):
        # make prompt
        enemy = internal_index[data["enemy_id"]]
        data["enemy_name"] = enemy["name"]
        data["enemy_type1"] = enemy["type1"]
        data["enemy_type2"] = enemy["type2"]
        data["percentage_hp"] = (data["enemy_hp"] / data["enemy_maxhp"]) * 100 # The robort can't dirctly get enemy's hp.

        my = internal_index[data["my_id"]]
        data["my_name"] = my["name"]
        data["my_type1"] = my["type1"]
        data["my_type2"] = my["type2"]


        move1 = move_index[data["my_move1"]]
        move2 = move_index[data["my_move2"]]
        move3 = move_index[data["my_move3"]]
        move4 = move_index[data["my_move4"]]

        data["move1_name"] = move1["name"]
        data["move1_type"] = move1["type"]
        data["move2_name"] = move2["name"]
        data["move2_type"] = move2["type"]
        data["move3_name"] = move3["name"]
        data["move3_type"] = move3["type"]
        data["move4_name"] = move4["name"]
        data["move4_type"] = move4["type"]

        return [{
            "role": "system",
            "content": system_prompt,
        },{
            "role": "user",
            'content': fight_template.render(data)
        }]
    
    def _act_move(self, move_index):
        self.pyboy.button_press('a',1)
        self.pyboy.tick()

        for i in range(self.lastfight-1):
            self.pyboy.button_press('up',1)
            self.pyboy.tick()

        for i in range(move_index-1):
            self.pyboy.button_press('down',1)
            self.pyboy.tick()

        self.pyboy.button_press('a',1)
        self.pyboy.tick()
        self.lastfight = move_index
    
    def _act_run(self):
        self.pyboy.button_press('down',1)
        self.pyboy.tick()
        self.pyboy.button_press('right',1)
        self.pyboy.tick()
        self.pyboy.button_press('a',1)
        self.pyboy.tick()

    def act(self, response):
        # use response to do some act
        response = json.loads(response)
        if response["decision"] == "run":
            self._act_run()
        else:
            self._act_move(response["decision"])
    
    def ifight(self):
        return bool(self.pyboy.memory[0xD057]) # Fight Flag
    
    def getresult(self):
        ...

    def start(self):
        print("# start fight")
        while self.ifight():
            tmp = self.read_data()
            if tmp['enemy_maxhp']  == 0:
                self.pyboy.button_press("a",1)
                self.pyboy.tick()
                continue
            self.act(get_chatgpt_response(self.dump_data(tmp)))

            self.pyboy.tick(100,True)

        print("# end fight")
        return self.getresult() # return fight result


def do_fight(pyboy_obj:PyBoy):
    return Fight(pyboy_obj).start()