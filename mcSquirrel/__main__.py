# mcSquirrel/main.py
import os
import platform

def find_minecraft_folder():
    # Determine the OS
    system = platform.system()

    if system == "Windows":
        # Try the default Windows location
        minecraft_path = os.path.join(os.getenv('APPDATA'), '.minecraft')
    elif system == "Darwin":  # macOS
        # Try the default macOS location
        minecraft_path = os.path.expanduser('~/Library/Application Support/minecraft')
    else:
        # Assume Linux or other Unix-based system
        minecraft_path = os.path.expanduser('~/.minecraft')

    # Check if the directory exists
    if os.path.isdir(minecraft_path):
        return minecraft_path
    else:
        # Ask the user to manually input the path
        print("Minecraft folder not found. Please provide the path manually.")
        user_path = input("Enter the Minecraft folder path: ")

        # Check if the provided path is valid
        if os.path.isdir(user_path):
            return user_path
        else:
            print("The provided path is not valid. Please try again.")
            return find_minecraft_folder()

def main():
    print("Hello World from McSquirrel!")
    print(f"Minecraft installation: {find_minecraft_folder()}")

if __name__ == "__main__":
    main()
