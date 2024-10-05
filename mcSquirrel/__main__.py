from .setup import load_setup
from .player import Player
from .logger import log, handle_error
from pprint import pprint
import json

def pretty_print_dataclass(dataclass_instance):
    if hasattr(dataclass_instance, 'data'):
        data_dict = dataclass_instance.data
        try:
            # Attempt to pretty print using JSON for better readability
            print(json.dumps(data_dict, indent=4))
        except TypeError:
            # Fallback to pprint if JSON serialization fails
            pprint(data_dict)
    else:
        pprint(dataclass_instance)

def main():
    try:
        log("Starting McSquirrel application...")
        print("Hello World from McSquirrel!")

        setup = load_setup()
        log("Loaded setup configuration successfully.")
        print("Minecraft installation:")
        pprint(setup)

        player = Player(setup, "c514c901-baae-4c8f-a377-6289fc358fd1")
        log("Loaded player data successfully.")

        log("Killing the player...")
        player.kill()
        log("Player has been killed successfully.")

    except Exception as e:
        handle_error(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()