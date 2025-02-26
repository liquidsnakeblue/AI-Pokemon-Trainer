# AI Pokemon Trainer

## Installtion

Firstly, you need install some package, use pip tool to install.

```bash
pip install -r requirements.txt
```

Then you need copy secret_setting.json.example to secret_setting.json, and typing the AI's api information.

## Usage

There are cli tools in the root folder, `cli.py`.

Run `python3 cli.py server`, you will get a web server which started in 8000 port and 18080 port used by websockets, it have beautiful screen. It's goal is for the normal user to watch how AI work.

Run `python3 cli.py local`, you will get a window that run by pyboy, you can see some detial in the console. It's goal is for test the AI.

![](./docs/img.png)

## Ablation Study

There are some cli option that you can setting which one will be removed.

- Remove Escape Unit `--remove-escape`
- Remove Switch Pokemon Unit `--remove-switch`

## Reference

[Pokémon Red and Blue/Internal Index Number](https://tcrf.net/Pok%C3%A9mon_Red_and_Blue/Internal_Index_Number)

[Pokémon Red and Blue/RAM map](https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Red_and_Blue/RAM_map)