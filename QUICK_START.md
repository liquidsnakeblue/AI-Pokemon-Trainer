# Quick Start Guide - Building the Executable

## For Windows Users

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Download the Source Code**
   - Get the project files
   - Extract to a folder (e.g., `C:\PokemonAI`)

3. **Run the Build Script**
   - Open Command Prompt in the project folder
   - Run: `build_executable.bat`
   - Wait for the build to complete (~5-10 minutes)

4. **Configure the Executable**
   - Go to `dist\PokemonAITrainer\`
   - Copy your Pokemon Red ROM to `roms\red.gb`
   - Copy `config\config.json.example` to `config\config.json`
   - Edit `config\config.json` with your OpenAI API key

5. **Run the Program**
   ```cmd
   cd dist\PokemonAITrainer
   PokemonAITrainer.exe server
   ```
   - Open browser to http://localhost:8000

## For Linux/Mac Users

1. **Install Python 3** (usually pre-installed)
   ```bash
   python3 --version
   ```

2. **Download and Extract Source Code**
   ```bash
   cd ~/Downloads
   # Extract the project files
   cd AI-Pokemon-Trainer
   ```

3. **Run the Build Script**
   ```bash
   chmod +x build_executable.sh
   ./build_executable.sh
   ```

4. **Configure the Executable**
   ```bash
   cd dist/PokemonAITrainer
   cp config/config.json.example config/config.json
   nano config/config.json  # Edit with your API key
   # Copy ROM to roms/red.gb
   ```

5. **Run the Program**
   ```bash
   ./PokemonAITrainer server
   ```
   - Open browser to http://localhost:8000

## Troubleshooting

### Build Fails
- Ensure Python 3.8+ is installed
- Run: `pip install -r requirements.txt` manually
- Check for error messages in the build output

### "ROM Not Found"
- Ensure ROM is named exactly `red.gb` (lowercase)
- Place in the `roms/` folder

### "API Error"
- Check your API key in `config/config.json`
- Verify you have API credits
- Test the API key at https://platform.openai.com/

### Executable Won't Run
- **Windows**: Install Visual C++ Redistributable
- **Linux**: Install SDL2: `sudo apt install libsdl2-2.0-0`
- **Mac**: Install SDL2: `brew install sdl2`

## What You Get

After building, you'll have a standalone application that:
- ✅ Runs without Python installed
- ✅ Has organized folders for ROMs and saves
- ✅ Uses a simple JSON config file
- ✅ Can be distributed to others (without ROM/API key)
- ✅ Works in web browser or native window mode

## Distribution Package Structure

```
PokemonAITrainer/
├── PokemonAITrainer.exe     ← Main program
├── config/
│   └── config.json          ← Your API settings
├── roms/
│   └── red.gb              ← Your Pokemon ROM
├── saves/
│   └── red.gb.state        ← Auto-saved progress
└── README.md               ← Full documentation
```

## Next Steps

1. **Read the full documentation**: `README.md` in the distribution folder
2. **Configure advanced options**: See command-line flags
3. **Test the AI**: Start a battle and watch it play!

## Build Options

### Create a Single-File Executable
Edit `build_exe.spec` and change:
```python
exe = EXE(..., onefile=True)
```
Then rebuild. This creates one .exe file instead of a folder.

### Reduce File Size
Exclude test files by editing `build_exe.spec`:
```python
excludes=['test', 'test_record', 'data_analyze'],
```

### Add an Icon
Place your `.ico` file in the project folder and edit `build_exe.spec`:
```python
icon='pokemon_icon.ico',
```

## Support

For detailed build instructions, see `BUILD_INSTRUCTIONS.md`

---

**Happy Building!** 🎮🤖