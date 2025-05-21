import json
import pathlib
import random

import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from scipy.stats import norm
import matplotlib.patheffects as path_effects


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


def token_distribution(data_list):
    token_list = []
    for data in data_list:
        for battle in data:
            token_list.append(battle["total_usage_token"])
    token_array = np.array(token_list)
    mean = np.mean(token_array)
    sigma = np.std(token_array, ddof=1)

    x = np.linspace(mean - 3 * sigma, mean + 3 * sigma, 100)
    pdf = norm.pdf(x, loc=mean, scale=sigma)
    bins = np.linspace(min(token_list), max(token_list), 10)
    counts, bin_edges = np.histogram(token_list, bins=bins)

    plt.hist(token_list, bins=bins, color='g', alpha=0.6, label='Histogram')
    pdf_counts = pdf * (bin_edges[1] - bin_edges[0]) * len(token_list)
    plt.plot(x, pdf_counts, color='r', label='Estimated Normal Distribution')

    plt.xlim(min(token_list), max(token_list))
    plt.xlabel("$token$")
    plt.ylabel("$counts$")
    plt.legend(loc="best")
    plt.show()


def single_operation_distribution(data):
    user_input = input()
    count = 0
    for battle in data:
        for operation in battle["rounds"][-1]["operation_history"]:
            if operation["operation"] == user_input:
                count += 1
    return user_input, count


def operation_distribution(data, count_lists, fig, ax):
    operation_counts = {}
    unit_topics = ["Cave", "", "", "", ""]
    for i in data:
        countlist = []
        user_input, count = single_operation_distribution(i)
        countlist.append(count)
        count_lists.append(countlist)
        operation_counts[user_input] = countlist

    name_lists = list(operation_counts)
    print(name_lists)

    bottom_2 = np.add(count_lists[0], count_lists[1])
    bottom_3 = np.add(bottom_2, count_lists[2])
    bottom_4 = np.add(bottom_3, count_lists[3])

    # create plot here
    ax.bar(range(len(count_lists[0])), count_lists[0],
           color="#D6E3B7", label=name_lists[0])
    ax.bar(range(len(count_lists[1])), count_lists[1],
           bottom=count_lists[0], color="#95A96A", label=name_lists[1])
    ax.bar(range(len(count_lists[2])), count_lists[2],
           bottom=bottom_2, color="#869E7A", label=name_lists[2])
    ax.bar(range(len(count_lists[3])), count_lists[3],
           bottom=bottom_3, color="#45602D", label=name_lists[3])
    ax.bar(range(len(count_lists[4])), count_lists[4],
           bottom=bottom_4, color="#AB9A6F", label=name_lists[4])
    ax.set_xticks(range(len(name_lists)))
    ax.set_xticklabels(unit_topics)
    ax.set_title("Counts Distribution")
    ax.set_xlabel("Fighting Place")
    ax.set_ylabel("Counts")
    ax.legend()
    ax.show()


def mean_bar_plot(fig, ax, mean_list, se_list, topics_list, color_list):

    round_mean_list = np.round(mean_list, decimals=3)
    ax.set_xlabel("Model")
    ax.set_ylabel("Percentage of Battles Won")
    ax.errorbar(topics_list, round_mean_list, color='#1f77b4', alpha=0.8,
                yerr=se_list, fmt="_", ecolor='black', capsize=5)
    bars = ax.bar(topics_list, round_mean_list, color=color_list)

    barlabel = ax.bar_label(bars, label_type="center", size=10, color="white")
    for text in barlabel:
        text.set_path_effects([
            path_effects.Stroke(linewidth=1, foreground="black"),
            path_effects.Normal(),
        ])

    ax.spines['top'].set_visible(False)

    ax.spines['right'].set_visible(False)
    ax.plot(1, 0, ">k", transform=ax.transAxes, markersize=8, clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.transAxes, markersize=8, clip_on=False)
    fig.autofmt_xdate()

    plt.show()


fig = plt.figure()
ax = fig.subplots()

BASE_DIR = pathlib.Path(__file__).parent.parent / "test_record"
COLOR_LIST = [
    "#2A3F54", "#4C6A92", "#6C8EBF", "#3E5F8A", "#5B7D9E",
    "#7F9DBD", "#4A708B", "#6E7B8B", "#8FBC8F", "#556B2F"
]

model_list = []
topics_list = []
color_list = []

list_path = pathlib.Path(__file__).parent / "data_file_paths.json"

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
