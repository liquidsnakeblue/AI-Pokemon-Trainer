import logging, time, yaml, os, json, datetime
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
            if os.getenv('AI_POKEMON_TRAINER_SKIP_ANIMATION') == '0':
                time.sleep(0.01)
            self.pyboy.press_and_release('left')
            if os.getenv('AI_POKEMON_TRAINER_SKIP_ANIMATION') == '0':
                time.sleep(0.01)

            if bool(self.pyboy.memory[0xD057]):
                return do_fight(self.pyboy)

def run_test(count, pyboy):
    logger.info("Test started")
    cnt = 0
    report = []
    logname = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(BASE_DIR / "test_record" / f"{logname}.{os.getenv('AI_POKEMON_TRAINER_TEST_SETTING')}.json", "w") as fp:
        for i in range(count):
            cnt+=1
            pyboy.total_usage_token = 0
            res, last_operation = TestFight(pyboy).run()
            logger.info(f"Test Process: {cnt}/{count}")
            report.append({
                "id": i,
                "total_usage_token": pyboy.total_usage_token,
                "last_operation": last_operation,
                "rounds": res,
            })
            fp.seek(0)
            fp.write(json.dumps(report, indent=4, separators=(',', ': '), ensure_ascii=True))
            fp.flush()
            os.fsync(fp.fileno())
    return report