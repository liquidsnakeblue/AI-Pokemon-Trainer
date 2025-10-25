# Pokemon AI Trainer - Executable Distribution

## Overview

This is the standalone executable distribution of the Pokemon AI Trainer program. The AI uses OpenAI's API to play Pokemon Red automatically.

## Directory Structure

```
PokemonAITrainer/
├── PokemonAITrainer.exe    # Main executable
├── config/                  # Configuration files
│   └── config.json.example  # Example configuration
├── roms/                    # Place your ROM file here
│   └── red.gb              # Pokemon Red ROM (not included)
├── saves/                   # Save states directory
│   └── red.gb.state        # Auto-generated save states
├── static/                  # Web UI assets (included)
├── templates/               # Web UI templates (included)
└── README.txt              # Quick start guide
```

## Setup Instructions

### 1. Add Your Pokemon Red ROM

Place your legally obtained Pokemon Red ROM file in the `roms/` folder:
- File name must be: `red.gb`
- This is the Game Boy ROM file for Pokemon Red

### 2. Configure API Settings

1. Copy `config/config.json.example` to `config/config.json`
2. Edit `config/config.json` with your API credentials:

```json
{
    "api-key": "your-openai-api-key-here",
    "base-url": "https://api.openai.com/v1",
    "model": "gpt-4"
}
```

**API Settings:**
- `api-key`: Your OpenAI API key (required)
- `base-url`: API endpoint URL (default: https://api.openai.com/v1)
- `model`: AI model to use (e.g., "gpt-4", "gpt-3.5-turbo")

### 3. Run the Program

Open Command Prompt or PowerShell in the `PokemonAITrainer` directory and run:

## Usage

### Web Server Mode (Recommended)

Start the web interface:

```cmd
PokemonAITrainer.exe server
```

Then open your browser to: **http://localhost:8000**

**Options:**
- `--port INTEGER`: HTTP server port (default: 8000)
- `--addr TEXT`: Listen address (default: 0.0.0.0)
- `--ws-port INTEGER`: WebSocket port (default: 18080)
- `--no-auto`: Disable automatic AI battles (manual control only)
- `--skip-animation`: Skip battle animations for faster gameplay
- `--debug`: Enable debug logging

**Examples:**

```cmd
# Run on different port
PokemonAITrainer.exe server --port 9000

# Run with animations disabled
PokemonAITrainer.exe server --skip-animation

# Manual control mode (no AI)
PokemonAITrainer.exe server --no-auto

# Debug mode
PokemonAITrainer.exe server --debug
```

### Local Window Mode

Run with PyBoy's native window (SDL2):

```cmd
PokemonAITrainer.exe local
```

This opens a Game Boy window directly on your desktop.

## Features

### Automatic AI Battle System
- AI automatically detects battles and makes decisions
- Uses OpenAI's API to analyze battle state and choose actions
- Supports attacking, switching Pokemon, using items, and running

### Web Interface
- Live Game Boy screen streaming via WebSocket
- Real-time party Pokemon status display
- Manual control with keyboard or on-screen buttons
- Save/Load state functionality
- AI decision display (action, reason, status)

### Save States
- Automatic save state management in `saves/` folder
- Save/Load via web interface or keyboard shortcuts
- Persistent game progress

## Keyboard Controls (Web Interface)

- **Arrow Keys**: D-Pad movement
- **Z**: A button
- **X**: B button
- **Enter**: Start
- **Shift**: Select

## Troubleshooting

### "ROM file not found"
- Ensure `red.gb` is in the `roms/` folder
- Check the file name is exactly `red.gb` (lowercase)

### "API Error" or "Authentication Failed"
- Verify your API key in `config/config.json`
- Check that the `base-url` is correct
- Ensure you have API credits available

### Web interface won't load
- Check that port 8000 is not already in use
- Try running on a different port: `--port 9000`
- Ensure firewall isn't blocking the connection

### Executable won't run
- Install Visual C++ Redistributable if needed
- Check Windows Defender/antivirus isn't blocking it
- Run as Administrator if permission errors occur

### AI isn't making moves
- Check the web interface shows "Thinking..." status
- Verify API configuration is correct
- Check debug logs with `--debug` flag

## Advanced Options

### Test Mode

Run automated battle tests:

```cmd
PokemonAITrainer.exe server --fight-test --test-count 10
```

### Ablation Studies

Disable specific AI capabilities:

```cmd
# Disable running from battles
PokemonAITrainer.exe server --remove-escape

# Disable Pokemon switching
PokemonAITrainer.exe server --remove-switch

# Disable item usage
PokemonAITrainer.exe server --remove-item
```

## Requirements

- Windows 10 or later (64-bit)
- Internet connection (for OpenAI API)
- Pokemon Red ROM file (not included)
- OpenAI API key
- ~500MB disk space

## Legal Notice

This software requires a legally obtained Pokemon Red ROM file. The ROM is NOT included with this distribution. You must own a legal copy of Pokemon Red to use this software.

## Support

For issues, questions, or contributions, visit the project repository.

## Credits

- PyBoy: Game Boy emulator
- OpenAI: API for AI decision making
- Flask: Web framework
- WebSockets: Real-time communication

---

**Version**: 1.0  
**Build Date**: 2025

Enjoy watching the AI play Pokemon!