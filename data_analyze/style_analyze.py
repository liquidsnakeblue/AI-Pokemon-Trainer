import json
import pathlib
import random
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats



def process_model_data(model_list):

    category_name = []
    result = {
        "test_list0": [] , 
        "test_list1": [] ,
        "test_list2": [] ,
        "test_list3": [],
        "test_list4": [],
        "test_list5" :[],
        "test_list6": []
    }
    
    for i in range(len(model_list)-1):
        for json_data in model_list[i]:
            
            for item in json_data:
                decision = item["last_operation"]["decision"]
                if decision not in category_name:
                    category_name.append(decision)
                    for key in result:
                        result[key].append(0)
                    result[f"test_list{i}"][-1] = result[f"test_list{i}"][-1] + 1 
                elif decision in category_name:
                    num = category_name.index(decision)
                    result[f"test_list{i}"][num] = result[f"test_list{i}"][num] + 1 

                for tmp in item["rounds"][-1]["operation_history"]: 
                    operation = tmp["operation"]

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

plt.show()


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


def survey(results, category_names):
    for key, value in results.items():
        tmp = np.sum(value)
        for i in range(len(value)):
            results[key][i] = results[key][i] / tmp

    labels = list(results.keys())
    data = np.array(list(results.values()))
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
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    plt.show()
    return fig, ax
    

survey(results, category_names)
