import json
import pathlib
import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import matplotlib.patheffects as path_effects

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

            test_battle_list.append(rounds_count/50)

        model_battle_list.append(test_battle_list)

    return model_battle_list
def get_mean_level(model_list):
    num = 0
    time = 0
    for test_list in model_list:
        for data in test_list:
            for battle in data:
                num+=battle["rounds"][-1]["enemy_level"]
                time+=1
    print(num/time)

def get_mean_and_se(model_battle_list):
    mean_list = []
    se_list = []
    for test_battle_list in model_battle_list:
        mean = np.mean(test_battle_list)
        se = stats.sem(test_battle_list)
        mean_list.append(mean)
        se_list.append(se)
    return mean_list, se_list


def get_sub_battle(data_list):
    res = []
    for data in data_list:
        battle_count = 0
        for battle in data:
            for op in battle["rounds"][-1]["operation_history"]:
                if op["operation"] != "run":
                    battle_count += 1
        res.append(battle_count)
    return res


def mean_bar_plot(fig, ax, mean_list, se_list, topics_list, color_list):

    round_mean_list = np.round(mean_list, decimals=3)
    ax.set_xlabel("Model")
    ax.set_ylabel("Percentage of Battles Won")
    ax.errorbar(topics_list, round_mean_list, color='#1f77b4', alpha=0.8,
                yerr=se_list, fmt="_", ecolor='black', capsize=5)
    #human test
    round_list=np.insert(round_mean_list, 0 , 0.86)
    print(round_list)
    se_list.insert(0,0)
    topics_list.insert(0,"Experienced\n Human Player")
    bars = ax.bar(topics_list, round_list, color=color_list, alpha=0.6)

    for bar, fill_color in zip(bars, color_list):
        rgba = to_rgba(fill_color)
        darker_color = (rgba[0]*0.7, rgba[1]*0.7, rgba[2]*0.7, 0.9)
        bar.set_edgecolor(darker_color)
        bar.set_hatch('/')
        bar.set_linewidth(1.2)

    barlabel = ax.bar_label(bars, label_type="center", size=10, color="black")
    for text, color in zip(barlabel, color_list):
        rgba = to_rgba(color)

        # if (rgba[0]/255) * (rgba[1]/255) * (rgba[2]/255) < 0.5:
        #     text.set_color("white")
        # else:
        #     text.set_color("black")

    ax.spines['top'].set_visible(False)

    ax.spines['right'].set_visible(False)
    ax.plot(1, 0, ">k", transform=ax.transAxes, markersize=8, clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.transAxes, markersize=8, clip_on=False)
    fig.autofmt_xdate()
    top_labels = ["N/A",1405,1369,1352,1338,1265,"N/A","N/A","N/A"]
    if top_labels is not None:
        ax_top = ax.twiny() 
        ax_top.set_xlim(ax.get_xlim())
        ax_top.set_xticks(np.arange(len(topics_list))) 
        ax_top.set_xticklabels(top_labels)
        ax_top.spines['top'].set_position(('outward', 10))
        ax_top.tick_params(axis='x', which='both', length=0) 
    ax_top.set_xlabel("LLM Arena Score")
    ax_top.plot(0, 1, "^k", transform=ax.transAxes, markersize=8, clip_on=False)
    ax_top.spines['right'].set_visible(False)

fig = plt.figure()
ax = fig.subplots()

BASE_DIR = pathlib.Path(__file__).parent.parent / "test_record"

model_list = []
topics_list = []
color_list = []
score_list = []

list_path = pathlib.Path(__file__).parent / "data_file_paths.json"

with open(list_path, "r", encoding="utf-8") as file:
    whole_list = json.loads(file.read())

    for model_name_list in whole_list:

        test_list = []
        topics_list.append(model_name_list["name"])
        color_list.append(model_name_list["color"])
        score_list.append(model_name_list["score"])

        color_list.append("darkgrey")

        for test_name in model_name_list["case"]:
            file_path = (BASE_DIR / test_name).resolve()

            if not file_path.exists():
                print("The file does not exist.", file_path)
                exit(0)

            with open(file_path, "r", encoding="utf-8") as file:
                test_list.append((json.loads(file.read())))

        model_list.append(test_list)

    print(len(model_list))

model_battle_list = get_battle(model_list)
get_mean_level(model_list)
print("The number of valid run:", model_battle_list)

mean_list, se_list = get_mean_and_se(model_battle_list)
mean_bar_plot(fig, ax, mean_list, se_list, topics_list, color_list)

ax.grid(axis='y', color='gray', linestyle='-', alpha=0.2)
plt.show()

#plt.savefig('output.png', dpi=300, bbox_inches='tight', transparent=True)