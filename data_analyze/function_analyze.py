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

    round_mean_list = np.round(mean_list, decimals=3)
    ax.set_xlabel("Model")
    ax.set_ylabel("Percentage of Battles Won")
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
    "#1ba784", "#e2c17c", "#2f90b9", "#ea8958", "#bacf65",
    "#ffa60f", "#813c85", "#248067", "#617172"]

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
