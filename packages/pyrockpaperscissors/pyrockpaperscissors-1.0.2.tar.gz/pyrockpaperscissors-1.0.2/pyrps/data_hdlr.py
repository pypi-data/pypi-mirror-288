import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

STATS_FILE = os.path.join(script_dir, 'stats.json')
DEFAULT_STATS = {
    "wins": 0,
    "losses": 0,
    "ties": 0,
    "games_played": 0
}

def load_stats():
    """Loads the stats data from the `stats.json` file."""
    if not os.path.exists(STATS_FILE):
        return DEFAULT_STATS
    
    try:
        with open(STATS_FILE, "r") as file:
            stats = json.load(file)
            if not all(key in stats for key in DEFAULT_STATS):
                raise ValueError("\n"
                                 "Missing keys in the stats.json file.")
            
            if not all(isinstance(stats[key], int) for key in stats):
                raise ValueError("\n"
                                 "Invalid value types in the stats.json file.")
            
            return stats
        
    except (json.JSONDecodeError, ValueError):
        return DEFAULT_STATS
    

def save_stats(stats):
    """Dumps the provided data into the `stats.json` file."""
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)
        
    
def repair_game():
    """Loads the data from `stats.json` and rewrites it. If the config data is broken, it will get replaced with the default configuration data template."""
    stats = load_stats()
    save_stats(stats)
    print("\n"
          "Game repaired! Stats file has been successfully validated.")
    input("\n"
          "Press any key to continue...")