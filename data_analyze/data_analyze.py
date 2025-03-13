import json
from pathlib import Path


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


def 
def main():
    user_path = input()
    file_path = Path(user_path).resolve()
    if not file_path.exists():
        print("The file does not exist.")
        return
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    print(get_rounds(data))

if __name__ == "__main__":
    main()

