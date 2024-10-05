import os
import platform
import json

# Constants
DATA_DIR = "../data"
SETUP_FILE = os.path.join(DATA_DIR, "setup.json")

# Logging Helper
def log(message):
    print(f"[LOG]: {message}")

# Error Handling Helper
def handle_error(message):
    print(f"[ERROR]: {message}")

# Check if a file exists
def file_exists(file_path):
    if os.path.isfile(file_path):
        log(f"File exists: {file_path}")
        return True
    else:
        log(f"File does not exist: {file_path}")
        return False

# Find Minecraft folder based on OS, or ask user to input manually
def find_minecraft_folder():
    log("Determining the operating system...")
    system = platform.system()

    if system == "Windows":
        minecraft_path = os.path.join(os.getenv('APPDATA'), '.minecraft')
        log("Detected Windows, trying default path...")
    elif system == "Darwin":  # macOS
        minecraft_path = os.path.expanduser('~/Library/Application Support/minecraft')
        log("Detected macOS, trying default path...")
    else:
        minecraft_path = os.path.expanduser('~/.minecraft')
        log("Detected Linux/Unix, trying default path...")

    # Check if the directory exists
    if os.path.isdir(minecraft_path):
        log(f"Minecraft folder found at: {minecraft_path}")
        return minecraft_path
    else:
        log("Minecraft folder not found at default location. Asking user for the path.")
        return ask_user_for_minecraft_path()

# Ask the user for the Minecraft folder path
def ask_user_for_minecraft_path():
    while True:
        user_path = input("Enter the Minecraft folder path: ")
        if os.path.isdir(user_path):
            log(f"Valid Minecraft path provided: {user_path}")
            return user_path
        else:
            handle_error("The provided path is not valid. Please try again.")

# Create the setup file
def create_setup():
    log("Creating new setup configuration...")
    minecraft_path = find_minecraft_folder()

    setup = {
        "version": 1.0,
        ".minecraft": {
            "mc_path": minecraft_path,
            "saves": os.path.join(minecraft_path, 'saves')
        }
    }

    write_setup(setup)

# Load the setup file
def load_setup():
    log("Checking for existing user setup...")

    if not os.path.exists(DATA_DIR):
        log(f"Data directory does not exist, creating: {DATA_DIR}")
        os.makedirs(DATA_DIR)

    if not file_exists(SETUP_FILE):
        log(f"Setup file not found at: {SETUP_FILE}, assuming new installation or corruption.")
        create_setup()
        return

    log("Setup file found, loading configuration...")
    try:
        with open(SETUP_FILE, "r") as setup_file:
            setup = json.load(setup_file)
            log(f"Loaded setup: {setup}")
            return setup
    except Exception as e:
        handle_error(f"Failed to load setup file: {e}")
        create_setup()

# Write setup to the file
def write_setup(setup):
    log("Writing setup to file...")
    try:
        with open(SETUP_FILE, "w") as setup_file:
            json.dump(setup, setup_file, indent=4)
        log(f"Setup written successfully to {SETUP_FILE}")
    except Exception as e:
        handle_error(f"Failed to write setup file: {e}")
