import json
import pathlib
import random
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats


def get_std_decision(tmp):
    if tmp[0] == "i":
        return "item"
    
    if tmp[0] == "s":
        return "switch"
    
    if tmp == "run":
        return "run"
    
    return f"move{tmp}"


def process_model_data(model_list):

    category_name = [
        "move1",
        "move2",
        "move3",
        "move4",
        "item",
        "switch",
        "run",
    ]
    result = {
        "test_list0": [0, 0, 0, 0, 0, 0, 0], 
        "test_list1": [0, 0, 0, 0, 0, 0, 0],
        "test_list2": [0, 0, 0, 0, 0, 0, 0],
        "test_list3": [0, 0, 0, 0, 0, 0, 0],
        "test_list4": [0, 0, 0, 0, 0, 0, 0],
        "test_list5" :[0, 0, 0, 0, 0, 0, 0],
        "test_list6": [0, 0, 0, 0, 0, 0, 0]
    }
    
    for i in range(len(model_list)-1):
        for json_data in model_list[i]:
            
            for item in json_data:
                decision = get_std_decision(item["last_operation"]["decision"])
                if decision not in category_name:
                    category_name.append(decision)
                    for key in result:
                        result[key].append(0)
                    result[f"test_list{i}"][-1] = result[f"test_list{i}"][-1] + 1 
                elif decision in category_name:
                    num = category_name.index(decision)
                    result[f"test_list{i}"][num] = result[f"test_list{i}"][num] + 1 

                for tmp in item["rounds"][-1]["operation_history"]: 
                    operation = get_std_decision(tmp["operation"])

                    if operation in category_name:
                        c = category_name.index(operation)
                        result[f"test_list{i}"][c] += 1
                    else:
                        category_name.append(operation)
                        for key in result:
                            result[key].append(0)
                            result[f"test_list{i}"][-1] = 1
    print(category_name)
    return category_name, result



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
category_names, results = process_model_data(model_list)



"""category_names = ['Strongly disagree', 'Disagree',
                  'Neither agree nor disagree', 'Agree', 'Strongly agree']
results = {
    'Question 1': [10, 15, 17, 32, 26],
    'Question 2': [26, 22, 29, 10, 13],
    'Question 3': [35, 37, 7, 2, 19],
    'Question 4': [32, 11, 9, 15, 33],
    'Question 5': [21, 29, 5, 5, 40],
    'Question 6': [8, 19, 5, 30, 38]
}"""


def survey(results, category_names, min_width_for_label=0.05):
    for key, value in results.items():
        tmp = np.sum(value)
        for i in range(len(value)):
            results[key][i] = results[key][i] / tmp

    labels = topics_list
    data = np.round(np.array(list(results.values())), decimals=2)
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        mask = widths > 0
        filtered_labels = [lab for lab, m in zip(labels, mask) if m]
        filtered_widths = widths[mask]
        filtered_starts = starts[mask]
        
        rects = ax.barh(filtered_labels, filtered_widths, 
                        left=filtered_starts, 
                        height=0.5,
                        label=colname, 
                        color=color)
        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for rect, width in zip(rects, filtered_widths):
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + rect.get_height() / 2
            
            ax.text(x, y, f'{width:.0%}',
                    ha='center', va='center',
                    color=text_color, fontsize=8)

    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    # plt.show()
    return fig, ax

CATEGORY_FRIEND_NAMES = {
    "move1": "Move 1",
    "move2": "Move 2",
    "move3": "Move 3",
    "move4": "Move 4",
    
    "switch": "Switch",
    "item": "Item",
    "run": "Run",
}

for i in range(len(category_names)):
    category_names[i] = CATEGORY_FRIEND_NAMES[category_names[i]]

survey(results, category_names)

# plt.show()

plt.savefig('output.png', dpi=300, bbox_inches='tight', transparent=True)