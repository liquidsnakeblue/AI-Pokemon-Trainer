# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Build & Run Commands

```bash
pip install -r requirements.txt
cp secret_setting.json.example secret_setting.json  # Edit with API keys
python3 cli.py server  # Web UI on port 8000, WebSocket on 18080
python3 cli.py local   # PyBoy window mode
```

## Critical Non-Obvious Patterns

- **Memory addresses are hex WITHOUT 0x prefix in fight.py** - `pyboy.memory[0xD057]` not `pyboy.memory['D057']`
- **Multi-byte values use [`connect_digit_list()`](engine/component.py:22)** - HP/stats span 2 addresses, must be combined with this function
- **Fight detection flag is at 0xD057** - `bool(pyboy.memory[0xD057])` triggers AI battle logic
- **Animation skipping requires memory check** - `pyboy.memory[0xc4f2]==238` indicates text box ready for advance
- **Party Pokemon slot IDs are 1-6, NOT 0-5** - All switch/item commands use 1-based indexing
- **Item usage format is "i<id> <pokemon_id>"** - e.g., `"i4 2"` uses item 4 on Pokemon 2 (space-separated, NOT "i4_2")
- **Ablation flags disable features silently** - Check `AI_POKEMON_TRAINER_ABLATION_*` env vars before expecting escape/switch/item
- **Test configs are YAML with hex keys** - `0xCFE6: 0` sets memory directly (see test/data/*.yaml)

## Environment Variables for Control

```bash
AI_POKEMON_TRAINER_FIGHT_TEST=1        # Enable test mode
AI_POKEMON_TRAINER_BASE_LINE=1         # Random baseline (not AI)
AI_POKEMON_TRAINER_SKIP_ANIMATION=1    # Skip delays
AI_POKEMON_TRAINER_NO_AUTO=1           # Manual control only
AI_POKEMON_TRAINER_ABLATION_ESCAPE=1   # Disable escape
AI_POKEMON_TRAINER_ABLATION_SWITCH=1   # Disable switching
AI_POKEMON_TRAINER_ABLATION_ITEM=1     # Disable items
```

## Code Style

- Use `logger.info()` not `print()` - Logger configured in app.py/main.py
- OpenAI client expects `response_format={"type": "json_object"}` - Hardcoded in api.py
- Jinja2 templates for prompts - Located in engine/prompt/*.txt
- PyBoy operations need tick() cycles - 10 ticks before/after button press/release

## Testing

- Run single test: `python3 cli.py server --fight-test --test-setting 001_simple --test-count 1`
- Test configs: `test/data/<name>.yaml` - Memory address overrides only
- Results saved: `test_record/<timestamp>.<test_setting>.json`