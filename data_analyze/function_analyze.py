import json
import pathlib
import random

import numpy as np
import matplotlib.pyplot as plt

from scipy import stats


def get_battle(model_list):
    model_battle_list = []
    for test_list in model_list:
        test_battle_list = []
        for data in test_list:
            rounds_count = 0
            for battle in data:
                Flag = True
                if battle["last_operation"]["decision"] == "run":
                    Flag = False
                if Flag:
                    rounds_count += 1
            test_battle_list.append(rounds_count/50)
        model_battle_list.append(test_battle_list)
    return model_battle_list


def get_mean_and_se(model_battle_list):
    mean_list = []
    se_list = []
    for test_battle_list in model_battle_list:
        mean = np.mean(test_battle_list)
        se = stats.sem(test_battle_list)
        mean_list.append(mean)
        se_list.append(se)
    return mean_list, se_list


def mean_bar_plot(fig, ax, mean_list, se_list, topics_list, color_list):

    round_mean_list = np.round(mean_list, decimals=2)
    ax.set_xlabel("Model")
    ax.set_ylabel("Percentage of Battles Won, (%)")
    ax.errorbar(topics_list, round_mean_list, color='#1f77b4', alpha=0.8,
                yerr=se_list, fmt="_", ecolor='black', capsize=5)
    bars = ax.bar(topics_list, round_mean_list, color=color_list)
    fig.autofmt_xdate()
    ax.bar_label(bars, label_type="center")
    plt.show()


fig = plt.figure()
ax = fig.subplots()

BASE_DIR = pathlib.Path(__file__).parent.parent / "test_record"
COLOR_LIST = [
    "#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33F3",
    "#33FFF3", "#F333FF", "#FFD700", "#4B0082", "#00FFFF",
    "#FF69B4", "#8A2BE2", "#ADFF2F", "#DA70D6", "#FF4500",
    "#2E8B57", "#FFA500", "#20B2AA", "#FF1493", "#00CED1",
    "#FF00FF", "#8B008B", "#00FF00", "#0000FF", "#FFFF00",
    "#FF0000", "#7CFC00", "#FFFACD", "#ADD8E6", "#F08080",
    "#E6E6FA", "#FF6347", "#4682B4", "#FFFFE0", "#00FF7F",
    "#20B2AA", "#FFB6C1", "#FFE4C4", "#FFDEAD", "#98FB98",
    "#AFEEEE"
]

model_list = []
topics_list = []
color_list = []

list_path = pathlib.Path(__file__).parent / "function_file_paths.json"

with open(list_path, "r", encoding="utf-8") as file:
    whole_list = json.loads(file.read())

    for model_name_list in whole_list:

        test_list = []
        topics_list.append(model_name_list["name"])
        color_list.append(random.choice(COLOR_LIST))

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
print("The number of valid run:", model_battle_list)

mean_list, se_list = get_mean_and_se(model_battle_list)
mean_bar_plot(fig, ax, mean_list, se_list, topics_list, color_list)
