# Board Game Arena Stats Scraper

A Python script for scraping Regicide game statistics from Board Game Arena, specifically designed for analyzing game outcomes and settings.

## Features

- Scrapes table numbers from game statistics page
- Collects detailed game settings for each table:
    - Hand size
    - Health modifier
    - Attack modifier
    - Difficulty level
    - Game outcome (won/lost based on enemies defeated)
- Handles disabled modifications game mode with default values
- Exports data to CSV format
- Includes progress tracking and error handling

## Prerequisites

- Python 3.x
- Chrome browser
- ChromeDriver (matching your Chrome version)
- Selenium WebDriver

## Required Python Packages

```bash
pip install -r requirements.txt
```

## Setup

1. Install Chrome browser if not already installed
2. Download ChromeDriver that matches your Chrome version
3. Copy `config.example.py` to `config.py` and update with your settings
4. Start Chrome with remote debugging enabled:

   ```bash
   /path/to/your/chrome.exe --remote-debugging-port=9222
   ```

    1. MacOS:

    ```bash
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   ```

## Configuration

The project uses a configuration file to manage personal settings:

1. Create your `config.py` file:

   ```bash
   cp config.example.py config.py
   ```

2. Update the values in `config.py`:
   - `CHROMEDRIVER_PATH`: Path to your ChromeDriver executable
   - `TARGET_URL`: Your BGA stats page URL

Note: `config.py` is gitignored to protect your personal information. Never commit this file to version control.

## Usage

1. Ensure you're logged into Board Game Arena in the Chrome instance
2. Run the script:

   ```bash
   python BGA_Scraper.py
   ```

3. The script will:
   - Collect table numbers from the stats page
   - Visit each table to collect game details
   - Save results to `regicide_raw_data.csv`

## Output Format

The script generates a CSV file with the following columns:
- table_number
- hand_size
- health_modifier
- attack_modifier
- difficulty
- game_won (1 for win, 0 for loss)

## Game Mode Details

- Normal Mode:
    - Collects actual values for all game settings
    - Determines win/loss based on enemies defeated count
  
- Disabled Mode (gameoption_100 = 'Disabled'):
    - Sets hand_size = 0
    - Sets health_modifier = 0
    - Sets attack_modifier = 0
    - Sets difficulty = 1
    - Still tracks game outcome

## Error Handling

- Prints progress updates to console
- Continues processing if individual table scraping fails
- Reports any errors during scraping process

## Project Structure

```
.
├── README.md
├── bga_scraper.py
├── config.example.py
├── config.py (created locally, not in repo)
└── .gitignore
```

## Limitations

- Requires manual Chrome session with remote debugging
- Depends on specific CSS selectors and page structure
- May need updates if BGA changes their website structure
- Limited to games where victory condition is 12 enemies defeated

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## Future Improvements

1. Change script to work for any game
2. Develop a dynamic CSS selector tool
