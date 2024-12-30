from pyboy import PyBoy
from .api import get_chatgpt_response
from .component import connect_digit_list
from .index_data import *
from jinja2 import Template
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

fight_template = None
with open(BASE_DIR / "engine" / "prompt" / "fight.txt", "r") as fp:
    fight_template = Template(fp.read())

class Fight:

    def __init__(self, pyboy_obj):
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
            "enemy_hp": connect_digit_list(self.pyboy.memory[0xCFE6:0xCFE7]),
            "enemy_maxhp": connect_digit_list(self.pyboy.memory[0xCFF4:0xCFF5]),
            "enemy_attack": connect_digit_list(self.pyboy.memory[0xCFF6:0xCFF7]),
            "enemy_defense": connect_digit_list(self.pyboy.memory[0xCFF8:0xCFF9]),
            "enemy_level": self.pyboy.memory[0xCFF0],
            "enemy_status": self.pyboy.memory[0xCFE9],

            "my_id": self.pyboy.memory[0xD014],
            "my_hp": self.pyboy.memory[0xD015:0xD016],
            "my_status": self.pyboy.memory[0xD018],
            "my_type1": self.pyboy.memory[0xD019],
            "my_type2": self.pyboy.memory[0xD01A],
            "my_move1": self.pyboy.memory[0xD01C],
            "my_move2": self.pyboy.memory[0xD01D],
            "my_move3": self.pyboy.memory[0xD01E],
            "my_move4": self.pyboy.memory[0xD01F],
            "my_maxhp": connect_digit_list(self.pyboy.memory[0xD023:0xD024]),
            "my_attack": connect_digit_list(self.pyboy.memory[0xD025:0xD026]),
            "my_defense": connect_digit_list(self.pyboy.memory[0xD027:0xD028]),
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
        data["percentage_hp"] = data["enemy_hp"] / data["enemy_maxhp"] # The robort can't dirctly get enemy's hp.

        my = internal_index[data["my_id"]]
        data["my_name"] = my["name"]
        data["my_type1"] = my["type1"]
        data["my_type2"] = my["type2"]

        return fight_template.render(data)
    
    def act(self, response):
        # use response to do some act
        ...
    
    def ifight(self):
        return bool(self.pyboy.memory[0xD057]) # Fight Flag
    
    def getresult(self):
        ...

    def start(self):
        print("# start fight")
        while self.ifight():

            # self.act(get_chatgpt_response(self.dump_data(self.read_data())))

            self.pyboy.tick(3600,True)

        print("# end fight")
        return self.getresult() # return fight result


def do_fight(pyboy_obj:PyBoy):
    return Fight(pyboy_obj).start()