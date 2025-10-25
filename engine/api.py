import os, json, shutil
from openai import OpenAI
from pathlib import Path

import logging
logger = logging.getLogger("ai_pokemon_trainer")

BASE_DIR = Path(__file__).resolve().parent.parent

# Import config loader for executable support
try:
    from config_loader import load_config, get_config_path
    SECRET_SETTING = load_config()
    # If config is empty, try fallback to old method
    if not SECRET_SETTING.get("api-key"):
        if not os.path.exists(BASE_DIR / 'secret_setting.json'):
            shutil.copyfile(BASE_DIR / 'secret_setting.json.example',
                            BASE_DIR / 'secret_setting.json')
        with open(BASE_DIR / 'secret_setting.json', 'r') as fp:
            SECRET_SETTING = json.loads(fp.read())
except ImportError:
    # Fallback to old config loading if config_loader not available
    SECRET_SETTING = None
    if not os.path.exists(BASE_DIR / 'secret_setting.json'):
        shutil.copyfile(BASE_DIR / 'secret_setting.json.example',
                        BASE_DIR / 'secret_setting.json')
    with open(BASE_DIR / 'secret_setting.json', 'r') as fp:
        SECRET_SETTING = json.loads(fp.read())

client = OpenAI(
    api_key=SECRET_SETTING["api-key"],
    base_url=SECRET_SETTING["base-url"],
)

def get_ai_response(prompt, cnt=1):
    logger.debug(f"Send to API, {json.dumps(prompt, indent=4, separators=(',', ': '), ensure_ascii=False)}")
    try:
        response = client.chat.completions.create(
            model=SECRET_SETTING["model"],
            messages=prompt,
            response_format={"type": "json_object"},
        )
    except Exception as e:
        if cnt>3:
            raise BaseException(f"Request API ERROR, and ther is no pssibility of countinue. STOP!")
        logger.error(f"Request API ERROR: {e}, Retry {cnt}!")
        return get_ai_response(prompt, cnt+1)
    logger.debug(f"Recived by API, {json.dumps(response.choices[0].message.content, indent=4, separators=(',', ': '), ensure_ascii=False)}")
    logger.info(f"API token usage: {response.usage.total_tokens}")
    return response.choices[0].message.content, response.usage.total_tokens
