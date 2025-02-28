import logging, time, json
from engine.fight import do_fight

logger = logging.getLogger("ai_pokemon_trainer")

class TestFight:
    def __init__(self, pyboy):
        self.pyboy = pyboy
    
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