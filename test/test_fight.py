import logging, time, yaml, os
from pathlib import Path
from engine.fight import do_fight

BASE_DIR = Path(__file__).resolve().parent.parent

logger = logging.getLogger("ai_pokemon_trainer")

class FightConfig:
    def __init__(self, config):
        with open(BASE_DIR / "test" / "data" / f"{config}.yaml") as fp:
            self.config = yaml.load(fp.read(), Loader=yaml.FullLoader)
    
    def __call__(self, pyboy):
        for i,j in self.config.items():
            pyboy.memory[i] = j

class TestFight:
    def __init__(self, pyboy):
        self.pyboy = pyboy
        self.pyboy.pre_fight_test = FightConfig(os.getenv('AI_POKEMON_TRAINER_TEST_SETTING', '001_simple'))
    
    def run(self):
        while True:
            self.pyboy.press_and_release('right')
            time.sleep(0.01)
            self.pyboy.press_and_release('left')
            time.sleep(0.01)

            if bool(self.pyboy.memory[0xD057]):
                return do_fight(self.pyboy)

def run_test(count, pyboy):
    logger.info("Test started")
    cnt = 0
    report = []
    for i in range(count):
        cnt+=1
        res = TestFight(pyboy).run()
        logger.info(f"Test Process: {cnt}/{count}")
        report.append({
            "id": i,
            "init_state": res[0],
            "result": res[-1],
        })
    return report