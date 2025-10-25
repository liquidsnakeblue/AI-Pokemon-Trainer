#!/bin/bash
# Build script for Pokemon AI Trainer Executable (Linux/Mac)

echo "========================================"
echo "Pokemon AI Trainer - Build Script"
echo "========================================"
echo ""

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller not found. Installing..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "Failed to install PyInstaller!"
        exit 1
    fi
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies!"
    exit 1
fi

echo ""
echo "Building executable..."
pyinstaller build_exe.spec --clean
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

echo ""
echo "Creating distribution folder structure..."
mkdir -p "dist/PokemonAITrainer/roms"
mkdir -p "dist/PokemonAITrainer/saves"
mkdir -p "dist/PokemonAITrainer/config"

echo ""
echo "Copying configuration files..."
cp "secret_setting.json.example" "dist/PokemonAITrainer/config/config.json.example"
if [ -f "red.gb" ]; then
    cp "red.gb" "dist/PokemonAITrainer/roms/"
fi

echo ""
echo "Copying README..."
cp "DISTRIBUTION_README.md" "dist/PokemonAITrainer/README.md"

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "The executable is located in: dist/PokemonAITrainer/"
echo ""
echo "Next steps:"
echo "1. Copy your Pokemon Red ROM to dist/PokemonAITrainer/roms/red.gb"
echo "2. Configure dist/PokemonAITrainer/config/config.json"
echo "3. Run PokemonAITrainer from the command line"
echo ""