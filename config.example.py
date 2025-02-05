# config.example.py
# Copy this file to config.py and update with your values
# Make sure to add config.py to .gitignore

CHROMEDRIVER_PATH = '/path/to/your/chromedriver'
TARGET_URL = "https://boardgamearena.com/gamestats?player=YOUR_PLAYER_ID&game_id=1606&finished=1"

# To only get details for a specific opponent use:
TARGET_URL = "https://boardgamearena.com/gamestats?player=YOUR_PLAYER_ID&opponent_id=OPPONENT_ID&game_id=1606&finished=1"