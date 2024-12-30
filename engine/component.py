import math

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