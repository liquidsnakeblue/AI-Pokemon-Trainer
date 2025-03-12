import json
file_path = "E:\保护动物隋欣航\青岛中学\python文件\\20250310_141740.002_ViridianForest.json"


def get_rounds(data):
    round =0
    for i in data:
        Flag = True
        for j in i["result"]["other_pokemon"]:
            if j["hp"]!=0:
                Flag = False
                break
        if not Flag:
            round+=1
    return round


with open(file_path, "r", encoding="utf-8") as file:
    data = json.loads(file.read())

print(get_rounds(data))