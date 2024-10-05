from .nbt import load_dat_file, DatEntry
from .logger import log, handle_error
from .git import commit_changes
import nbtlib
import os

class Player:
    def __init__(self, setup: dict, player_uid: str):
        try:
            log(f"Initializing Player with UID: {player_uid}")
            self.setup = setup
            self.player_uid = player_uid

            # Find paths to player.dat and level.dat files
            self.player_file_path = self._find_player_file()
            self.level_file_path = self._find_level_file()

            self.player_data = load_dat_file(self.player_file_path)
            self.level_data = None

            if not self.player_data.data:
                handle_error("Failed to load player data. Player data is empty.")
            else:
                log("Player data loaded successfully.")

            # Determine whether to use level.dat based on game mode
            self.single_player_mode = self._is_single_player()
            if self.single_player_mode:
                log("Single-player mode detected. Loading level.dat for additional edits.")
                self.level_data = load_dat_file(self.level_file_path)
            else:
                log("Multiplayer mode detected. Editing only player-specific data.")
        except Exception as e:
            handle_error(f"Failed to initialize player: {e}")

    def _find_player_file(self):
        try:
            saves_path = self.setup['.minecraft']['saves']
            playerdata_dir = os.path.join(saves_path, 'x', 'playerdata')
            player_file_path = os.path.join(playerdata_dir, f"{self.player_uid}.dat")
            if os.path.exists(player_file_path):
                log(f"Found player file at: {player_file_path}")
                return player_file_path
            else:
                raise FileNotFoundError(f"Player file not found for UID: {self.player_uid}")
        except Exception as e:
            handle_error(f"Error finding player file: {e}")
            raise

    def _find_level_file(self):
        try:
            saves_path = self.setup['.minecraft']['saves']
            level_file_path = os.path.join(saves_path, 'x', 'level.dat')
            if os.path.exists(level_file_path):
                log(f"Found level.dat file at: {level_file_path}")
                return level_file_path
            else:
                raise FileNotFoundError("level.dat file not found.")
        except Exception as e:
            handle_error(f"Error finding level.dat file: {e}")
            raise

    def _is_single_player(self):
        try:
            # Check if level.dat exists to determine if it's single-player
            if os.path.exists(self.level_file_path):
                playerdata_dir = os.path.dirname(self.player_file_path)
                player_files = [f for f in os.listdir(playerdata_dir) if f.endswith('.dat')]
                return len(player_files) == 1  # If there's only one player, it's single-player
            return False
        except Exception as e:
            handle_error(f"Error determining game mode: {e}")
            return False

    def kill(self):
        try:
            log("Preparing to kill player...")
            commit_changes("Committing changes before killing the player.")

            # Set health to zero
            self.player_data['Health'] = nbtlib.tag.Float(0.0)

            # Set other attributes to simulate death in hardcore mode
            self.player_data['DeathTime'] = nbtlib.tag.Short(20)  # Set death animation time
            self.player_data['HurtTime'] = nbtlib.tag.Short(10)  # Set hurt animation time
            self.player_data['playerGameType'] = nbtlib.tag.Int(3)  # Set to spectator mode to simulate hardcore death
            self.player_data['Dead'] = nbtlib.tag.Byte(1)  # Mark player as dead

            log("Player attributes set to simulate death.")

            # Save player data
            self.player_data.save(self.player_file_path)

            # If single-player, also edit the level.dat file
            if self.single_player_mode and self.level_data:
                log("Updating level.dat to reflect player death...")
                self.level_data['Data']['Player'] = self.player_data.data  # Update the Player tag in level.dat
                self.level_data.save(self.level_file_path)
                log("level.dat updated successfully.")
        except Exception as e:
            handle_error(f"Failed to kill player: {e}")

    def get_player_data(self):
        return self.player_data