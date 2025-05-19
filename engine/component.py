import math, json, re
from pathlib import Path
from jinja2 import Template
from random import choice

import logging
logger = logging.getLogger("ai_pokemon_trainer")

BASE_DIR = Path(__file__).resolve().parent.parent

def digit_number(num):
    if num == 0:
        return 1
    return int(math.log10(abs(num))) + 1


def connect_digit(num, num2):
    num*=(10**digit_number(num2))
    return num+num2


def connect_digit_list(numlist):
    res = numlist[0]
    for i in range(0,len(numlist)):
        res = connect_digit(res, numlist[i])
    return res


def read_prompt(name):
    template = None
    with open(BASE_DIR / "engine" / "prompt" / f"{name}.txt", "r", encoding = "utf-8") as fp:
        template = Template(fp.read())
    return template


def read_prompt_without_template(name):
    template = None
    with open(BASE_DIR / "engine" / "prompt" / f"{name}.txt", "r", encoding = "utf-8") as fp:
        template = fp.read()
    return template

def extract_json_from_string(input_string):
    json_pattern = r'\{(?:[^{}]|\{(?:[^{}])*\})*\}'
    match = re.search(json_pattern, input_string)
    if match:
        json_str = match.group()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(input_string)
            raise ValueError(f"Invalid JSON format: {e}")
    logger.error(input_string)
    raise ValueError(f"JSON format error")

def random_operation(data):
    ops = ["run", "s", "i", "move"]
    op = choice(ops)

    if op == "run":
        return {"decision": "run", "reason": "Random choose"}
    
    elif op == "s":
        return {"decision": "s" + str(choice(data["other_pokemon"])["id"]), "reason": "Random choose"}
    
    elif op == "i":
        for i in data["item"]:
            if i["name"] == "Potion" and i["quantity"] != 0:
                return {"decision": "i" + str(i["id"]), "reason": "Random choose"}
    
    return {"decision": choice(data["my_move"])["id"], "reason": "Random choose"}