import os
import mcpython
from .setup import load_setup
from .logger import log, handle_error

class Player:
    def __init__(self, setup: dict, player_uid: str):
        try:
            log(f"Initializing Player with UID: {player_uid}")
            self.setup = setup
            self.player_uid = player_uid

            # Locate the paths for player.dat and level.dat files
            self.player_file_path = self._find_player_file()
            self.level_file_path = self._find_level_file()

            # Load player data using specialized Minecraft library
            self.player_data = mcpython.load_player_data(self.player_file_path)
            self.level_data = None

            if self.player_data is None:
                handle_error("Failed to load player data. Player data is empty.")
            else:
                log("Player data loaded successfully.")

            # Detect single-player or multiplayer mode
            self.single_player_mode = self._is_single_player()
            if self.single_player_mode:
                log("Single-player mode detected. Loading level.dat for additional edits.")
                self.level_data = mcpython.load_level_data(self.level_file_path)
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
            # Determine single-player mode by checking the number of player files
            playerdata_dir = os.path.dirname(self.player_file_path)
            player_files = [f for f in os.listdir(playerdata_dir) if f.endswith('.dat')]
            return len(player_files) == 1  # If only one player file, assume single-player
        except Exception as e:
            handle_error(f"Error determining game mode: {e}")
            return False

    def kill(self):
        try:
            log("Preparing to kill player...")
            mcpython.commit_changes("Committing changes before killing the player.")

            # Set health and other necessary properties to simulate death
            self.player_data.set_health(0.0)
            self.player_data.set_death_time(20)
            self.player_data.set_hurt_time(10)
            self.player_data.set_game_mode('spectator')
            self.player_data.mark_as_dead()

            log("Player attributes set to simulate death.")

            # Save player data using the Minecraft API library
            mcpython.save_player_data(self.player_file_path, self.player_data)

            # If single-player, also update the level.dat file
            if self.single_player_mode and self.level_data:
                log("Updating level.dat to reflect player death...")
                self.level_data.update_player(self.player_uid, self.player_data)
                mcpython.save_level_data(self.level_file_path, self.level_data)
                log("level.dat updated successfully.")
        except Exception as e:
            handle_error(f"Failed to kill player: {e}")

    def get_player_data(self):
        return self.player_data

# Example usage
if __name__ == "__main__":
    setup = load_setup()
    player_uid = 'c514c901-baae-4c8f-a377-6289fc358fd1'
    player = Player(setup, player_uid)
    player.kill()
