"""
Configuration and file path management for the executable distribution
"""
import os
import sys
import json
from pathlib import Path

def get_base_dir():
    """Get the base directory for the application"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).resolve().parent

def get_config_path():
    """Get the configuration file path"""
    base_dir = get_base_dir()
    
    # Check for config in executable distribution structure
    config_paths = [
        base_dir / "config" / "config.json",
        base_dir / "secret_setting.json",
        Path(__file__).resolve().parent / "secret_setting.json"
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            return config_path
    
    # Return default path if none exist
    return config_paths[1]

def get_rom_path():
    """Get the ROM file path"""
    base_dir = get_base_dir()
    
    # Check for ROM in executable distribution structure
    rom_paths = [
        base_dir / "roms" / "red.gb",
        base_dir / "red.gb",
        Path(__file__).resolve().parent / "red.gb"
    ]
    
    for rom_path in rom_paths:
        if rom_path.exists():
            return str(rom_path)
    
    # Return default path
    return str(rom_paths[1])

def get_save_state_path():
    """Get the save state file path"""
    base_dir = get_base_dir()
    
    # Use saves directory in executable distribution
    saves_dir = base_dir / "saves"
    if not saves_dir.exists() and getattr(sys, 'frozen', False):
        saves_dir.mkdir(parents=True, exist_ok=True)
    
    if saves_dir.exists():
        return saves_dir / "red.gb.state"
    
    # Fallback to base directory
    return base_dir / "red.gb.state"

def load_config():
    """Load configuration from JSON file"""
    config_path = get_config_path()
    
    if not config_path.exists():
        return {
            "api-key": "",
            "base-url": "",
            "model": ""
        }
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config from {config_path}: {e}")
        return {
            "api-key": "",
            "base-url": "",
            "model": ""
        }