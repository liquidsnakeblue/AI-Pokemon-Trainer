from pyboy import PyBoy
from .api import get_chatgpt_response
from .component import (
    connect_digit_list, 
    read_prompt, 
    read_prompt_without_template,
    extract_json_from_string,
)
from .index_data import *

import logging
logger = logging.getLogger("ai_pokemon_trainer")

fight_template = read_prompt("fight")
system_prompt = read_prompt_without_template("system_prompt")

class Fight:

    def __init__(self, pyboy_obj):
        self.lastfight = 1
        self.pyboy = pyboy_obj
        self.history = []
    
    def press_and_release(self,key):
        for _ in range(10):
            self.pyboy.tick()
        self.pyboy.button_press(key)
        for _ in range(10):
            self.pyboy.tick()
        self.pyboy.button_release(key)
        for _ in range(10):
            self.pyboy.tick()
    
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
            "enemy_defense": connect_digit_list([self.pyboy.memory[0xCFF8],self.pyboy.memory[0xCFF9]]),
            "enemy_level": self.pyboy.memory[0xCFF3],
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
            "my_move2_pp": self.pyboy.memory[0xD02E],
            "my_move3_pp": self.pyboy.memory[0xD02F],
            "my_move4_pp": self.pyboy.memory[0xD030],

            "fight_mod": self.pyboy.memory[0xD057],

            "other_pokemon": [
                {
                    "id": 1,
                    "level": self.pyboy.memory[0xD18C],
                    "name_index":self.pyboy.memory[0xD164],
                    "hp": connect_digit_list([self.pyboy.memory[0xD16C], self.pyboy.memory[0xD16D]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD18F], self.pyboy.memory[0xD190]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD191], self.pyboy.memory[0xD192]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD1B9], self.pyboy.memory[0xD1BA]]),
                },
                {
                    "id": 2,
                    "level": self.pyboy.memory[0xD1B8],
                    "name_index":self.pyboy.memory[0xD165],
                    "hp": connect_digit_list([self.pyboy.memory[0xD198], self.pyboy.memory[0xD199]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD1BB], self.pyboy.memory[0xD1BC]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD1BD], self.pyboy.memory[0xD1BE]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD1BD], self.pyboy.memory[0xD1BE]]),
                },
                {
                    "id": 3,
                    "level": self.pyboy.memory[0xD1E4],
                    "name_index":self.pyboy.memory[0xD166],
                    "hp": connect_digit_list([self.pyboy.memory[0xD1C4], self.pyboy.memory[0xD1C5]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD1E7], self.pyboy.memory[0xD1E8]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD1E9], self.pyboy.memory[0xD1EA]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD1E5], self.pyboy.memory[0xD1E6]]),
                },
                {
                    "id": 4,
                    "level": self.pyboy.memory[0xD210],
                    "name_index":self.pyboy.memory[0xD167],
                    "hp": connect_digit_list([self.pyboy.memory[0xD1F0], self.pyboy.memory[0xD1F1]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD213], self.pyboy.memory[0xD214]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD191], self.pyboy.memory[0xD192]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD211], self.pyboy.memory[0xD212]]),
                },
                {
                    "id": 5,
                    "level": self.pyboy.memory[0xD18C],
                    "name_index":self.pyboy.memory[0xD168],
                    "hp": connect_digit_list([self.pyboy.memory[0xD21C], self.pyboy.memory[0xD21D]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD23F], self.pyboy.memory[0xD240]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD241], self.pyboy.memory[0xD242]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD23D], self.pyboy.memory[0xD23E]]),
                },
                {
                    "id": 6,
                    "level": self.pyboy.memory[0xD268],
                    "name_index":self.pyboy.memory[0xD169],
                    "hp": connect_digit_list([self.pyboy.memory[0xD248], self.pyboy.memory[0xD249]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD26B], self.pyboy.memory[0xD26C]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD26D], self.pyboy.memory[0xD26E]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD269], self.pyboy.memory[0xD26A]]),
                },
            ]
        }
    
    def dump_data(self, data):
        # make prompt
        enemy = internal_index[data["enemy_id"]]
        data["enemy_name"] = enemy["name"]
        data["enemy_type1"] = enemy["type1"]
        data["enemy_type2"] = enemy["type2"]
        data["percentage_hp"] = round((data["enemy_hp"] / data["enemy_maxhp"]) * 100) # The robort can't dirctly get enemy's hp.

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


        for i in data["other_pokemon"]: #To check which pokemon is in battle. Then tell AI which is the current pokemon.
            if i["level"] == data["my_level"] and i["name_index"] == data["my_id"] and i["hp"] == data["my_hp"]:
                data["now_pokemon_id"] = i["id"]
                break

        return [{
            "role": "system",
            "content": system_prompt,
        },{
            "role": "user",
            'content': fight_template.render(data)
        }]
    
    def _act_move(self, move_index):
        self.press_and_release('a')
        move_index=int(move_index)
        for i in range(self.lastfight-1):
            self.press_and_release('up')

        for i in range(move_index-1):
            self.press_and_release('down')

        self.press_and_release('a')
        self.lastfight = move_index
    
    def _act_run(self):
        self.press_and_release('down')
        self.press_and_release('right')
        self.press_and_release('a')

    def act(self, response):
        # use response to do some act
        response = extract_json_from_string(response)
        self.pyboy.run_data["reason_msg"] = response["reason"]
        if response["decision"] == "run":
            self.pyboy.run_data["action_msg"] = "Run"
            self._act_run()
        else:
            self.pyboy.run_data["action_msg"] = f"Use move {response['decision']}"
            self._act_move(response["decision"])
    
    def ifight(self):
        return bool(self.pyboy.memory[0xD057]) # Fight Flag
    
    def getresult(self):
        ...

    def start(self):
        self.pyboy.run_data["status_msg"] = "Started fighting"
        flag=True
        while self.ifight():
            # while self.pyboy.memory[0xC4F2] != 16 and self.ifight():
            #     logger.debug(f"** Skip msg")
            #     self.pyboy.run_data["action_msg"] = "Skip msg"
            #     self.pyboy.run_data["reason_msg"] = "..."
            #     self.press_and_release('a')
            
            #We could hard code the first keypress since it's always the same "A wild ... appears,"
            #Start of Battle
            #Render battle start animation
            if flag==True:
                for _ in range(360):
                    self.pyboy.tick()
                self.press_and_release('a')    
                #Render "throw pokemon out" animation
                for _ in range(360):
                    self.pyboy.tick()
                flag=False
            tmp = self.read_data()
            #What if the pokemon wants to learn a new skill?
            #End of Battle
            if tmp['enemy_maxhp']  == 0: 
                self.press_and_release('a')
                continue
            #logger.debug(f"Fight Data {tmp}")
            self.act(get_chatgpt_response(self.dump_data(tmp)))

            for _ in range(720):
                #We will need a check here for dialogues. If our pokemon uses a non-damaging move, critical hits, dialogue will pop-up and need to press a
                if self.pyboy.memory[0xC4F2]==238:
                    self.press_and_release('a')
                self.pyboy.tick()

        self.pyboy.run_data["status_msg"] = "Manual Operation"
        return self.getresult() # return fight result


def do_fight(pyboy_obj:PyBoy):
    return Fight(pyboy_obj).start()