import nbtlib
from dataclasses import dataclass, field
from typing import Any
from .logger import log, handle_error
from .git import commit_changes

@dataclass
class DatEntry:
    data: dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, key):
        try:
            if key in self.data:
                log(f"Accessing attribute '{key}' with value: {self.data[key]}")
                return self.data[key]
            else:
                handle_error(f"Attribute '{key}' not found in data.")
        except Exception as e:
            handle_error(f"Error accessing attribute '{key}': {e}")

    def __setitem__(self, key, value):
        try:
            log(f"Setting attribute '{key}' to value: {value}")
            self.data[key] = value
        except Exception as e:
            handle_error(f"Error setting attribute '{key}': {e}")

    def save(self, path: str):
        try:
            log(f"Saving NBT data to path: {path}")

            # Convert dictionary back to nbtlib Compound to ensure the correct format
            nbt_data = nbtlib.Compound(self.data)
            nbt_file = nbtlib.File({'': nbt_data})
            nbt_file.save(path)

            log("Successfully saved NBT data.")
            commit_changes(f"Saved changes to NBT data at {path}")
        except Exception as e:
            handle_error(f"Error saving NBT data to '{path}': {e}")


# Function to load a player's NBT .dat file
def load_dat_file(path: str) -> DatEntry:
    try:
        log(f"Loading NBT file from path: {path}")
        player_nbt = nbtlib.load(path)
        log("Successfully loaded NBT file.")

        player_data = dict(player_nbt)
        return DatEntry(data=player_data)
    except FileNotFoundError:
        handle_error(f"File not found: {path}")
    except Exception as e:
        handle_error(f"Error loading NBT file: {e}")

    return DatEntry()  # Return an empty DatEntry in case of failure
