import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def get_rounds(data):
    rounds_count = 0  
    Flag = True
    for battle in data:  
        for operation in battle["rounds"][-1]["operation_history"]:
            if operation["operation"]=="run":
                Flag = False
        if Flag:
            rounds_count+=1
    return rounds_count
def get_sub_battle(data):
    battle_count = 0
    for battle in data:
        for op in battle["rounds"][-1]["operation_history"]:
            try:
                int(op["operation"])
                battle_count += 1
            except ValueError:
                ...
    return battle_count

def token_distribution(data):
    token_list=[]
    for battle in data:
        token_list.append(battle["total_usage_token"])
    token_array=np.array(token_list)
    mean = np.mean(token_array)
    sigma = np.std(token_array,ddof=1)
    x = np.linspace(mean - 3 * sigma, mean + 3 * sigma, 100)
    pdf = norm.pdf(x, loc = mean, scale = sigma)
    plt.hist(token_list, bins=10)
    plt.plot(x, pdf, color='r', label='Estimated Normal Distribution')
    plt.xlim(400,2500)
    plt.xlabel("$token$")
    plt.ylabel("$count$")
    plt.show()

def main():
    user_path = input()
    file_path = Path(user_path).resolve()
    if not file_path.exists():
        print("The file does not exist.")
        return
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    print(get_sub_battle(data))
    print(get_rounds(data))
    token_distribution(data)

if __name__ == "__main__":
    main()

