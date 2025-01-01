import math
from pathlib import Path
from jinja2 import Template

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
    with open(BASE_DIR / "engine" / "prompt" / f"{name}.txt", "r") as fp:
        template = Template(fp.read())
    return template


def read_prompt_without_template(name):
    template = None
    with open(BASE_DIR / "engine" / "prompt" / f"{name}.txt", "r") as fp:
        template = fp.read()
    return template