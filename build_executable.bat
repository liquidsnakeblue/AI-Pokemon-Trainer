@echo off
REM Build script for Pokemon AI Trainer Windows Executable

echo ========================================
echo Pokemon AI Trainer - Build Script
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller!
        pause
        exit /b 1
    )
)

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo Building executable...
pyinstaller build_exe.spec --clean
if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Creating distribution folder structure...
if not exist "dist\PokemonAITrainer\roms" mkdir "dist\PokemonAITrainer\roms"
if not exist "dist\PokemonAITrainer\saves" mkdir "dist\PokemonAITrainer\saves"
if not exist "dist\PokemonAITrainer\config" mkdir "dist\PokemonAITrainer\config"

echo.
echo Copying configuration files...
copy "secret_setting.json.example" "dist\PokemonAITrainer\config\config.json.example" >nul
if exist "red.gb" copy "red.gb" "dist\PokemonAITrainer\roms\" >nul

echo.
echo Creating README...
(
echo Pokemon AI Trainer - Executable Version
echo ========================================
echo.
echo SETUP INSTRUCTIONS:
echo -------------------
echo 1. Place your Pokemon Red ROM file ^(red.gb^) in the 'roms' folder
echo 2. Copy config\config.json.example to config\config.json
echo 3. Edit config\config.json with your OpenAI API credentials:
echo    - api-key: Your OpenAI API key
echo    - base-url: API base URL ^(e.g., https://api.openai.com/v1^)
echo    - model: Model name ^(e.g., gpt-4^)
echo.
echo USAGE:
echo ------
echo Run the executable from command line with options:
echo.
echo Start Web Server Mode:
echo   PokemonAITrainer.exe server [OPTIONS]
echo.
echo   Options:
echo     --port INTEGER          HTTP server port ^(default: 8000^)
echo     --addr TEXT             Listen address ^(default: 0.0.0.0^)
echo     --ws-port INTEGER       WebSocket port ^(default: 18080^)
echo     --no-auto               Disable automatic AI play
echo     --skip-animation        Skip battle animations
echo     --debug                 Enable debug mode
echo.
echo Start Local Window Mode:
echo   PokemonAITrainer.exe local
echo.
echo SAVE FILES:
echo -----------
echo - Save states are stored in the 'saves' folder
echo - The default save file is 'red.gb.state'
echo.
echo TROUBLESHOOTING:
echo ----------------
echo - Ensure your ROM file is named 'red.gb' or update the code
echo - Check that config.json has valid API credentials
echo - For web mode, access http://localhost:8000 in your browser
echo.
echo For more information, visit the project repository.
) > "dist\PokemonAITrainer\README.txt"

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo The executable is located in: dist\PokemonAITrainer\
echo.
echo Next steps:
echo 1. Copy your Pokemon Red ROM to dist\PokemonAITrainer\roms\red.gb
echo 2. Configure dist\PokemonAITrainer\config\config.json
echo 3. Run PokemonAITrainer.exe from the command line
echo.
pause