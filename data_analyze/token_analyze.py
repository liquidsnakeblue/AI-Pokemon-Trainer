import json
import pathlib
import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

from scipy import stats
def get_battle(model_list):
    model_battle_list = []

    for test_list in model_list:
        test_battle_list = []

        for data in test_list:
            rounds_count = 0

            for battle in data:

                Flag = True
                Flag1 = False

                if battle["last_operation"]["decision"] == "run":
                    Flag = False

                for poke in battle["rounds"][-1]["other_pokemon"]:
                    if poke["hp"] != 0:
                        Flag1 = True
                        break

                if Flag and Flag1:
                    rounds_count += 1

            test_battle_list.append(rounds_count)

        model_battle_list.append(test_battle_list)

    return model_battle_list


def get_token(model_list,model_battle_list):
    token_list = []
    for test_list in model_list:
        test_token_list = []
        for data in test_list:
            token_count = 0
            for battle in data:
                token_count+=battle["total_usage_token"]
            test_token_list.append(token_count)
        token_list.append(test_token_list)
    for i in range(len(token_list)):
        for j in range(len(token_list[i])):
            if model_battle_list[i][j]==0:
                token_list[i].pop(j)
                model_battle_list[i].pop(j)
                i=i-1
                j=j-1
            token_list[i][j]=token_list[i][j]/(model_battle_list[i][j])
    return token_list

def get_mean_and_se(token_list):
    mean_list = []
    se_list = []
    token_list.pop(-1) #delete the baseline group since baseline is useless
    for test_token_list in token_list:
        mean = np.mean(test_token_list)
        se = stats.sem(test_token_list)
        mean_list.append(mean)
        se_list.append(se)
    return mean_list, se_list

def mean_bar_plot(fig, ax, mean_list, se_list, topics_list, color_list):

    round_mean_list = np.round(mean_list)
    ax.set_xlabel("Model")
    ax.set_ylabel("Average Token Usage Per Winning")
    topics_list.pop(-1) #delete the last group(baseline)
    ax.errorbar(topics_list, round_mean_list, color='#1f77b4', alpha=0.8,
                yerr=se_list, fmt="_", ecolor='black', capsize=5)
    bars = ax.bar(topics_list, round_mean_list, color=color_list, alpha=0.6)

    for bar, fill_color in zip(bars, color_list):
        rgba = to_rgba(fill_color)
        darker_color = (rgba[0]*0.7, rgba[1]*0.7, rgba[2]*0.7, 0.9)
        bar.set_edgecolor(darker_color)
        bar.set_hatch('/')
        bar.set_linewidth(1.2)

    barlabel = ax.bar_label(bars, label_type="center", size=10, color="black")


    ax.spines['top'].set_visible(False)

    ax.spines['right'].set_visible(False)
    ax.plot(1, 0, ">k", transform=ax.transAxes, markersize=8, clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.transAxes, markersize=8, clip_on=False)
    fig.autofmt_xdate()


fig = plt.figure()
ax = fig.subplots()

BASE_DIR = pathlib.Path(__file__).parent.parent / "test_record"

model_list = []
topics_list = []
color_list = []

list_path = pathlib.Path(__file__).parent / "data_file_paths.json"

with open(list_path, "r", encoding="utf-8") as file:
    whole_list = json.loads(file.read())

    for model_name_list in whole_list:

        test_list = []
        topics_list.append(model_name_list["name"])
        color_list.append(model_name_list["color"])

        for test_name in model_name_list["case"]:
            file_path = (BASE_DIR / test_name).resolve()

            if not file_path.exists():
                print("The file does not exist.", file_path)
                exit(0)

            with open(file_path, "r", encoding="utf-8") as file:
                test_list.append((json.loads(file.read())))

        model_list.append(test_list)

    print(len(model_list))

model_token_list = get_token(model_list,get_battle(model_list))
print("The number of valid run:", model_token_list)

mean_list, se_list = get_mean_and_se(model_token_list)
mean_bar_plot(fig, ax, mean_list, se_list, topics_list, color_list)

ax.grid(axis='y', color='gray', linestyle='-', alpha=0.2)
# plt.show()

plt.savefig('token_spent_for_each_model.png', dpi=300, bbox_inches='tight', transparent=True)