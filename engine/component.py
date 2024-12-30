import math
from pathlib import Path
from jinja2 import Template

BASE_DIR = Path(__file__).resolve().parent.parent

def digit_number(num):
    if n == 0:
        return 1
    return int(math.log10(abs(n))) + 1


def connect_digit(num, num2):
    num*=(10**digit_number(num2))
    return num+num2


def connect_digit_list(numlist):
    res = 0
    for i in range(len(numlist)-1):
        res = connect_digit(res, numlist[i+1])
    return res


def read_prompt(name):
    fight_template = None
    with open(BASE_DIR / "engine" / "prompt" / f"{name}.txt", "r") as fp:
        fight_template = Template(fp.read())
    return fight_template