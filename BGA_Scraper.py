import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from config import CHROMEDRIVER_PATH, TARGET_URL
except ImportError:
    print("Please create a config.py file with CHROMEDRIVER_PATH and TARGET_URL")
    print("You can copy config.example.py to config.py and update the values")
    exit(1)

def scrape_table_details(driver, table_number):
    try:
        print(f"Navigating to table number: {table_number}")
        driver.get(f"https://boardgamearena.com/table?table={table_number}")
        time.sleep(2)

        # Check if game option 100 is disabled
        game_option_100 = driver.find_element(By.ID, 'gameoption_100_displayed_value').text
        enemies_defeated = driver.find_element(By.CSS_SELECTOR, '#table_stats > div:nth-child(4) > div.row-value').text.strip()
        
        # Determine game outcome
        game_won = enemies_defeated == '12'
        
        print(f"Table {table_number}: Enemies Defeated = '{enemies_defeated}', Game Won = {game_won}")

        if game_option_100 == 'Disabled':
            details = {
                'table_number': table_number,
                'hand_size': 0,
                'health_modifier': 0,
                'attack_modifier': 0,
                'difficulty': 1,
                'game_won': int(game_won)
            }
            print(f"Table {table_number}: Disabled mode - default values")
        else:
            details = {
                'table_number': table_number,
                'hand_size': driver.find_element(By.ID, 'gameoption_101_displayed_value').text,
                'health_modifier': driver.find_element(By.ID, 'gameoption_103_displayed_value').text,
                'attack_modifier': driver.find_element(By.ID, 'gameoption_104_displayed_value').text,
                'difficulty': driver.find_element(By.CSS_SELECTOR, '#table_stats > div:nth-child(5) > div.row-value').text,
                'game_won': int(game_won)
            }
            print(f"Table {table_number}: Collecting full details")
        return details
    except Exception as e:
        print(f"Error scraping table {table_number}: {e}")
        return None

def scrape_table_numbers(target_url, chromedriver_path):
    print("Starting table number scraping process...")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print(f"Navigating to target URL: {target_url}\n")
        driver.get(target_url)
        table_numbers = set()
        max_clicks = 7
        clicks = 0

        while clicks < max_clicks:
            table_number_elements = driver.find_elements(By.CSS_SELECTOR, 'a.table_name.bga-link.smalltext')
            current_tables = {elem.text.strip('#') for elem in table_number_elements}
            
            print(f"Iteration {clicks + 1}: Found {len(current_tables)} new table numbers")
            table_numbers.update(current_tables)

            try:
                see_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "see_more_tables"))
                )
                see_more_button.click()
                clicks += 1
                time.sleep(2)
                print(f"    Clicked 'See more' button. Total unique tables: {len(table_numbers)}")
            except Exception:
                print("No more 'See more' button available or error occurred.")
                break

        print(f"\nScraping complete. Total unique table numbers collected: {len(table_numbers)}")
        return sorted(table_numbers)

    finally:
        driver.quit()

def scrape_table_details(driver, table_number):
    try:
        print(f"    Navigating to table number: {table_number}")
        driver.get(f"https://boardgamearena.com/table?table={table_number}")
        time.sleep(2)

        # Check if game option 100 is disabled
        game_option_100 = driver.find_element(By.ID, 'gameoption_100_displayed_value').text
        enemies_defeated = driver.find_element(By.CSS_SELECTOR, '#table_stats > div:nth-child(4) > div.row-value').text.strip()
        
        # Determine game outcome
        game_won = enemies_defeated == '12'
        
        if game_option_100 == 'Disabled':
            details = {
                'table_number': table_number,
                'hand_size': 0,
                'health_modifier': 0,
                'attack_modifier': 0,
                'difficulty': 1,
                'game_won': game_won
            }
            print(f"    Table {table_number}: Disabled mode - default values")
        else:
            details = {
                'table_number': table_number,
                'hand_size': driver.find_element(By.ID, 'gameoption_101_displayed_value').text,
                'health_modifier': driver.find_element(By.ID, 'gameoption_103_displayed_value').text,
                'attack_modifier': driver.find_element(By.ID, 'gameoption_104_displayed_value').text,
                'difficulty': driver.find_element(By.CSS_SELECTOR, '#table_stats > div:nth-child(5) > div.row-value').text,
                'game_won': game_won
            }
            print(f"    Table {table_number}: Collecting full details")
        return details
    except Exception as e:
        print(f"Error scraping table {table_number}: {e}")
        return None


def scrape_and_save_table_details(table_numbers, chromedriver_path, output_file='regicide_raw_data.csv'):
    print(f"Starting table details scraping for {len(table_numbers)} tables\n")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        all_details = []
        for i, table_number in enumerate(table_numbers, 1):
            print(f"Processing table {i}/{len(table_numbers)}: {table_number}")
            detail = scrape_table_details(driver, table_number)
            if detail:
                all_details.append(detail)

        if all_details:
            keys = all_details[0].keys()
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(all_details)
            print(f"Saved {len(all_details)} table details to {output_file}")
        else:
            print("No table details were collected.")

    finally:
        driver.quit()

if __name__ == "__main__":
    # Two-step process
    print("Starting Board Game Arena Scraper\n")
    table_numbers = scrape_table_numbers(TARGET_URL, CHROMEDRIVER_PATH)
    scrape_and_save_table_details(table_numbers, CHROMEDRIVER_PATH)
    print("\nScraping process completed.")
