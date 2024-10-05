# mcSquirrel/main.py
from .setup import load_setup


def main():
    print("Hello World from McSquirrel!")
    print(f"Minecraft installation: {load_setup()}")

if __name__ == "__main__":
    main()
