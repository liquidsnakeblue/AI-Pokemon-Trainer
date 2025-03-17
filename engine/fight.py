from pyboy import PyBoy
from .api import get_ai_response
from .component import (
    connect_digit_list, 
    read_prompt, 
    read_prompt_without_template,
    extract_json_from_string,
)
from .index_data import *

import logging, os
logger = logging.getLogger("ai_pokemon_trainer")

fight_template = read_prompt("fight")
system_prompt = read_prompt("system_prompt")

class Fight:

    def __init__(self, pyboy_obj):
        self.lastfight = 1 # Last time use move
        self.nowpoke = 1 # Last time use pokemon
        
        self.pyboy = pyboy_obj
        self.history = []
        self.operation_history = []
        self.round_cnt = 1

        self.is_ablation_escape = os.getenv('AI_POKEMON_TRAINER_ABLATION_ESCAPE', '0') == '1'
        if self.is_ablation_escape: logger.info('Ablation escape unit.')

        self.is_ablation_switch = os.getenv('AI_POKEMON_TRAINER_ABLATION_SWITCH', '0') == '1'
        if self.is_ablation_switch: logger.info('Ablation switch pokemon unit.')
    
    def press_and_release(self,key):
        """
        Automatic Press Button
        """
        for _ in range(10):
            self.pyboy.tick()
        self.pyboy.button_press(key)
        for _ in range(10):
            self.pyboy.tick()
        self.pyboy.button_release(key)
        for _ in range(10):
            self.pyboy.tick()
    
    def read_data(self):
        """
        Get Data from the game
        """

        logger.debug("Get Information about game.")
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
            "my_maxhp": connect_digit_list([self.pyboy.memory[0xD023],self.pyboy.memory[0xD024]]),
            "my_attack": connect_digit_list([self.pyboy.memory[0xD025],self.pyboy.memory[0xD026]]),
            "my_defense": connect_digit_list([self.pyboy.memory[0xD027],self.pyboy.memory[0xD028]]),
            "my_level": self.pyboy.memory[0xD022],

            "fight_mod": self.pyboy.memory[0xD057],

            "my_move": [
                {
                    "id": 1,
                    "index": self.pyboy.memory[0xD01C],
                    "pp": self.pyboy.memory[0xD02D],
                    "is_active": True,
                },
                {
                    "id": 2,
                    "index": self.pyboy.memory[0xD01D],
                    "pp": self.pyboy.memory[0xD02E],
                    "is_active": True,
                },
                {
                    "id": 3,
                    "index": self.pyboy.memory[0xD01E],
                    "pp": self.pyboy.memory[0xD02F],
                    "is_active": True,
                },
                {
                    "id": 4,
                    "index": self.pyboy.memory[0xD01F],
                    "pp": self.pyboy.memory[0xD030],
                    "is_active": True,
                }
            ],

            "other_pokemon": [
                {
                    "id": 1,
                    "level": self.pyboy.memory[0xD18C],
                    "name_index":self.pyboy.memory[0xD164],
                    "hp": connect_digit_list([self.pyboy.memory[0xD16C], self.pyboy.memory[0xD16D]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD18F], self.pyboy.memory[0xD190]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD191], self.pyboy.memory[0xD192]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD18D], self.pyboy.memory[0xD18E]]),
                    "experience": connect_digit_list([self.pyboy.memory[0xD179], self.pyboy.memory[0xD17A],self.pyboy.memory[0xD17B]]),
                    "is_active": True,
                },
                {
                    "id": 2,
                    "level": self.pyboy.memory[0xD1B8],
                    "name_index":self.pyboy.memory[0xD165],
                    "hp": connect_digit_list([self.pyboy.memory[0xD198], self.pyboy.memory[0xD199]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD1BB], self.pyboy.memory[0xD1BC]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD1BD], self.pyboy.memory[0xD1BE]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD1B9], self.pyboy.memory[0xD1BA]]),
                    "experience": connect_digit_list([self.pyboy.memory[0xD1A5], self.pyboy.memory[0xD1A6],self.pyboy.memory[0xD1A7]]),
                    "is_active": True,
                },
                {
                    "id": 3,
                    "level": self.pyboy.memory[0xD1E4],
                    "name_index":self.pyboy.memory[0xD166],
                    "hp": connect_digit_list([self.pyboy.memory[0xD1C4], self.pyboy.memory[0xD1C5]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD1E7], self.pyboy.memory[0xD1E8]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD1E9], self.pyboy.memory[0xD1EA]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD1E5], self.pyboy.memory[0xD1E6]]),
                    "experience": connect_digit_list([self.pyboy.memory[0xD1D1], self.pyboy.memory[0xD1D2],self.pyboy.memory[0xD1D3]]),
                    "is_active": True,
                },
                {
                    "id": 4,
                    "level": self.pyboy.memory[0xD210],
                    "name_index":self.pyboy.memory[0xD167],
                    "hp": connect_digit_list([self.pyboy.memory[0xD1F0], self.pyboy.memory[0xD1F1]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD213], self.pyboy.memory[0xD214]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD191], self.pyboy.memory[0xD192]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD211], self.pyboy.memory[0xD212]]),
                    "experience": connect_digit_list([self.pyboy.memory[0xD1FD], self.pyboy.memory[0xD1FE],self.pyboy.memory[0xD1FF]]),
                    "is_active": True,
                },
                {
                    "id": 5,
                    "level": self.pyboy.memory[0xD18C],
                    "name_index":self.pyboy.memory[0xD168],
                    "hp": connect_digit_list([self.pyboy.memory[0xD21C], self.pyboy.memory[0xD21D]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD23F], self.pyboy.memory[0xD240]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD241], self.pyboy.memory[0xD242]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD23D], self.pyboy.memory[0xD23E]]),
                    "experience": connect_digit_list([self.pyboy.memory[0xD229], self.pyboy.memory[0xD22A],self.pyboy.memory[0xD22B]]),
                    "is_active": True,
                },
                {
                    "id": 6,
                    "level": self.pyboy.memory[0xD268],
                    "name_index":self.pyboy.memory[0xD169],
                    "hp": connect_digit_list([self.pyboy.memory[0xD248], self.pyboy.memory[0xD249]]),
                    "attack": connect_digit_list([self.pyboy.memory[0xD26B], self.pyboy.memory[0xD26C]]),
                    "defense": connect_digit_list([self.pyboy.memory[0xD26D], self.pyboy.memory[0xD26E]]),
                    "max_hp": connect_digit_list([self.pyboy.memory[0xD269], self.pyboy.memory[0xD26A]]),
                    "experience": connect_digit_list([self.pyboy.memory[0xD255], self.pyboy.memory[0xD256],self.pyboy.memory[0xD257]]),
                    "is_active": True,
                },
            ]
        }
    
    def dump_data(self, data):
        """
        Make Prompt
        """

        logger.debug("Make Prompt.")
        # Enemy information
        enemy = internal_index[data["enemy_id"]]
        data["enemy_name"] = enemy["name"]
        data["enemy_type1"] = enemy["type1"]
        data["enemy_type2"] = enemy["type2"]
        data["percentage_hp"] = round((data["enemy_hp"] / data["enemy_maxhp"]) * 100) # The robort can't dirctly get enemy's hp.

        # Self information
        my = internal_index[data["my_id"]]
        data["my_name"] = my["name"]
        data["my_type1"] = my["type1"]
        data["my_type2"] = my["type2"]

        # Process Other Pokemon
        for i in range(6):
            if data["other_pokemon"][i]["level"] == 0 or data["other_pokemon"][i]["hp"] == 0:
                data["other_pokemon"][i]["is_active"] = False
                continue

            other_name = internal_index[data["other_pokemon"][i]["name_index"]]
            data["other_pokemon"][i]["name"] = other_name["name"]
        
        # Process Moves
        for i in range(4):
            if data["my_move"][i]["index"] == 0:
                data["my_move"][i]["is_active"] = False
                continue

            tmp = move_index[data["my_move"][i]["index"]]
            data["my_move"][i]["name"] = tmp["name"]
            data["my_move"][i]["type"] = tmp["type"]

        is_has_other_pokemon = False

        for i in data["other_pokemon"]: #To check which pokemon is in battle. Then tell AI which is the current pokemon.
            if i["level"] == data["my_level"] and i["name_index"] == data["my_id"] and i["hp"] == data["my_hp"]:
                data["now_pokemon_id"] = i["id"]
                self.nowpoke = i["id"]
            else:
                if i["hp"] != 0:
                    is_has_other_pokemon = True
        
        data["is_has_other_pokemon"] = is_has_other_pokemon
        
        data["ablation"] = {
            "escape": self.is_ablation_escape,
            "switch": self.is_ablation_switch,
        }

        self.history.append(data)

        data["operation_history"] = self.operation_history

        return [{
            "role": "system",
            "content": system_prompt.render(data),
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
    
    def _act_run_no_hp(self):
        self.press_and_release('down')
        self.press_and_release('a')
    
    def _act_switch_poke(self, poke_index):
        if self.read_data()["my_hp"] != 0:
            self.press_and_release('right')
            self.press_and_release('a')
        else:
            self.press_and_release('a')
        for i in range(self.nowpoke-1):
            self.press_and_release('up')
        for i in range(poke_index-1):
            self.press_and_release('down')
        self.press_and_release('a')
        self.press_and_release('a')
        self.nowpoke = poke_index

    def act(self, response):
        """
        Use response to do some act
        """

        logger.debug("Do Act.")
        self.pyboy.update_run_data("reason_msg", response["reason"])

        self.operation_history.append({
            "operation": response["decision"],
            "reason": response["reason"],
            "id": self.round_cnt,
        })
        self.round_cnt = self.round_cnt + 1

        if response["decision"] == "run" and (not self.is_ablation_escape):
            # Run
            self.pyboy.update_run_data("action_msg", "Run")
            logger.info("Act, run.")

            if self.read_data()["my_hp"] == 0:
                self._act_run_no_hp()
            else:
                self._act_run()
        elif response["decision"][0] == "s" and (not self.is_ablation_switch):
            # Switch Pokemon
            tmp = int(response["decision"][1:])
            self.pyboy.update_run_data("action_msg", f"Switch Pokemon: {tmp}")
            logger.info(f"Act, switch to {tmp}")

            self._act_switch_poke(tmp)
        elif response["decision"][0] == "e":
            # TODO: Use elements
            ...
        else:
            # Move
            self.pyboy.update_run_data("action_msg", f"Use move {response['decision']}")
            logger.info(f"Act, move {response['decision']}")

            self._act_move(response["decision"])
    
    def ifight(self):
        return bool(self.pyboy.memory[0xD057]) # Fight Flag
    
    def getresult(self):
        self.dump_data(self.read_data())
        return self.history

    def start(self):
        self.pyboy.update_run_data("status_msg", "Started fighting")
        logger.info("Started Fighting.")
        flag=True
        while self.ifight():
            self.pyboy.pre_fight_test(self.pyboy)
            # while self.pyboy.memory[0xC4F2] != 16 and self.ifight():
            #     logger.debug(f"** Skip msg")
            #     self.pyboy.update_run_data("action_msg", "Skip msg")
            #     self.pyboy.update_run_data("reason_msg", "...")
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

            self.pyboy.update_run_data("think_status", True)
            while True:
                response, used_token = get_ai_response(self.dump_data(tmp))
                self.pyboy.total_usage_token += used_token
                try:
                    response = extract_json_from_string(response)
                    break
                except ValueError as e:
                    logger.error(e)
                    logger.error("Resend!")
            self.act(response)
            self.pyboy.update_run_data("think_status", False)

            for _ in range(720):
                #We will need a check here for dialogues. If our pokemon uses a non-damaging move, critical hits, dialogue will pop-up and need to press a
                if self.pyboy.memory[0xC4F2]==238:
                    self.press_and_release('a')
                self.pyboy.tick()

        logger.info("End of Fighting.")
        self.pyboy.update_run_data("status_msg", "Manual Operation")
        return self.getresult() # return fight result


def do_fight(pyboy_obj:PyBoy):
    return Fight(pyboy_obj).start()
