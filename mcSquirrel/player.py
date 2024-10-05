from .nbt import load_dat_file, DatEntry
from .logger import log, handle_error
from .git import commit_changes
import nbtlib

class Player:
    def __init__(self, player_file_path: str):
        try:
            log(f"Initializing Player from file: {player_file_path}")
            self.player_file_path = player_file_path
            self.player_data = load_dat_file(player_file_path)
            if not self.player_data.data:
                handle_error("Failed to load player data. Player data is empty.")
            else:
                log("Player data loaded successfully.")
        except Exception as e:
            handle_error(f"Failed to initialize player: {e}")

    def kill(self):
        try:
            log("Preparing to kill player...")
            commit_changes("Committing changes before killing the player.")
            self.player_data['Health'] = nbtlib.tag.Float(0.0)  # Ensure health is set using proper NBT tag type
            log("Player has been killed.")
            self.player_data.save(self.player_file_path)
        except Exception as e:
            handle_error(f"Failed to kill player: {e}")

    def get_player_data(self):
        return self.player_data
