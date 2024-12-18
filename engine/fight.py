from pyboy import PyBoy
from .api import get_chatgpt_response
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
        ...
    
    def dump_data(self, data):
        # make prompt
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