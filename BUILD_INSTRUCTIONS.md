# Building the Pokemon AI Trainer Executable

## Overview

This guide explains how to build the Pokemon AI Trainer program into a standalone executable for Windows, Linux, or macOS.

## Prerequisites

1. **Python 3.8+** installed
2. **pip** package manager
3. All dependencies from `requirements.txt`
4. **PyInstaller** (will be installed automatically by build script)

## Quick Build

### Windows

1. Open Command Prompt or PowerShell
2. Navigate to the project directory
3. Run the build script:

```cmd
build_executable.bat
```

### Linux/macOS

1. Open Terminal
2. Navigate to the project directory
3. Make the script executable (first time only):

```bash
chmod +x build_executable.sh
```

4. Run the build script:

```bash
./build_executable.sh
```

## Manual Build Steps

If you prefer to build manually:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Build with PyInstaller

```bash
pyinstaller build_exe.spec --clean
```

### 3. Create Distribution Structure

```bash
# Windows
mkdir dist\PokemonAITrainer\roms
mkdir dist\PokemonAITrainer\saves
mkdir dist\PokemonAITrainer\config

# Linux/macOS
mkdir -p dist/PokemonAITrainer/roms
mkdir -p dist/PokemonAITrainer/saves
mkdir -p dist/PokemonAITrainer/config
```

### 4. Copy Configuration Files

```bash
# Windows
copy secret_setting.json.example dist\PokemonAITrainer\config\config.json.example
copy DISTRIBUTION_README.md dist\PokemonAITrainer\README.md

# Linux/macOS
cp secret_setting.json.example dist/PokemonAITrainer/config/config.json.example
cp DISTRIBUTION_README.md dist/PokemonAITrainer/README.md
```

## Output Structure

After building, you'll find the following structure in `dist/PokemonAITrainer/`:

```
PokemonAITrainer/
├── PokemonAITrainer.exe (or PokemonAITrainer on Linux/Mac)
├── config/
│   └── config.json.example
├── roms/
│   └── (place red.gb here)
├── saves/
│   └── (save states created automatically)
├── static/
├── templates/
├── engine/
└── _internal/ (PyInstaller dependencies)
```

## Customization

### Changing the Executable Icon

Edit `build_exe.spec` and set the `icon` parameter:

```python
exe = EXE(
    ...
    icon='path/to/icon.ico',  # Add your .ico file here
)
```

### Excluding Test Files

To reduce executable size, exclude test files by modifying `build_exe.spec`:

```python
excludes=['test', 'test_record', 'data_analyze'],
```

### Adding Additional Files

To include additional files in the distribution, add them to the `datas` list in `build_exe.spec`:

```python
datas=[
    ('static', 'static'),
    ('templates', 'templates'),
    ('your_file.txt', '.'),  # Add custom files here
] + pyboy_datas,
```

## Troubleshooting

### PyInstaller Import Errors

If PyInstaller can't find certain modules, add them to `hiddenimports` in `build_exe.spec`:

```python
hiddenimports = collect_submodules('pyboy') + [
    'your_missing_module',
]
```

### Large Executable Size

To reduce size:
1. Exclude unnecessary modules in `excludes` list
2. Use UPX compression (already enabled in spec file)
3. Remove debug symbols with `strip=True`

### Missing DLL Errors (Windows)

If the executable fails with missing DLL errors:
1. Install Visual C++ Redistributable
2. Add required DLLs to `binaries` in `build_exe.spec`

### SDL2 Window Issues

For the local window mode, ensure SDL2 libraries are included:
- Windows: SDL2.dll should be auto-detected
- Linux: Install `libsdl2-2.0-0` package
- macOS: Install SDL2 via Homebrew

## Distribution

### Creating a Zip Archive

```bash
# Windows
cd dist
tar -a -c -f PokemonAITrainer.zip PokemonAITrainer

# Linux/macOS
cd dist
tar -czf PokemonAITrainer.tar.gz PokemonAITrainer
```

### What to Include in Distribution

1. The entire `PokemonAITrainer/` folder
2. The `README.md` file (copied from DISTRIBUTION_README.md)
3. License information
4. Instructions for obtaining a legal ROM

**DO NOT** include:
- The Pokemon Red ROM file (users must provide their own)
- Your personal API keys
- Test data or development files

## Testing the Build

Before distributing:

1. Test the executable on a clean system without Python installed
2. Verify all features work:
   - Web server mode
   - Local window mode
   - Config loading from `config/config.json`
   - ROM loading from `roms/red.gb`
   - Save states in `saves/` directory
3. Test with different command-line options
4. Check that error messages are helpful

## Platform-Specific Notes

### Windows
- Build on Windows for best compatibility
- Executable name: `PokemonAITrainer.exe`
- Antivirus may flag the executable (false positive)

### Linux
- Build on the target distribution
- Executable name: `PokemonAITrainer`
- May need to set executable permission: `chmod +x PokemonAITrainer`

### macOS
- Build on macOS for macOS users
- May need to allow unsigned apps in System Preferences
- Consider code signing for wider distribution

## Build Optimization

For production builds:

1. Use `--onefile` for single executable (slower startup):
   ```bash
   pyinstaller build_exe.spec --onefile --clean
   ```

2. Disable console window (GUI mode only):
   ```python
   console=False,  # in build_exe.spec EXE section
   ```

3. Add version information (Windows):
   ```python
   version='version_info.txt',  # in build_exe.spec EXE section
   ```

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [PyBoy Documentation](https://docs.pyboy.dk/)
- Project repository for issues and updates

## Support

For build issues:
1. Check PyInstaller logs in `build/` directory
2. Run with `--debug all` flag for verbose output
3. Verify all dependencies are installed correctly
4. Check the project's issue tracker

---

**Last Updated**: 2025  
**PyInstaller Version**: 5.0+  
**Python Version**: 3.8+