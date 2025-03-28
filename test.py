import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import re

# File paths
input_file = r"D:\GPBudgetAnalysis\MadhyaPradesh_GP.xlsx"
output_file = r"D:\GPBudgetAnalysis\MadhyaPradesh_with_latlong.xlsx"

# Load village names from Excel
df = pd.read_excel(input_file)
village_names = df["Village Panchayat and Equivalent"].dropna().tolist()

# Load already processed villages if output file exists
if os.path.exists(output_file):
    processed_df = pd.read_excel(output_file, engine="openpyxl")
    processed_villages = set(processed_df["Village"].dropna().tolist())
else:
    processed_df = pd.DataFrame(columns=["Village", "Google Maps URL", "Latitude", "Longitude"])
    processed_villages = set()

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless") 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def extract_lat_long(url):
    """Extract latitude and longitude from Google Maps URL."""
    match = re.search(r'@([-.\d]+),([-.\d]+)', url)
    if match:
        return match.group(1), match.group(2)  # (latitude, longitude)
    return None, None  # Return None if not found

def search_village(village_name, retries=1):
    """Search for a village in Google Maps and return the final URL with retries."""
    driver.get("https://www.google.com/maps")
    time.sleep(2)  # Allow initial page load

    for attempt in range(retries):
        try:
            print(f"🔍 Attempt {attempt+1}: Searching {village_name}")

            # Clear and type village name
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#searchboxinput"))
            )
            search_box.clear()
            search_box.send_keys(village_name)

            # Click the search button
            search_button = driver.find_element(By.CSS_SELECTOR, "#searchbox-searchbutton > span")
            search_button.click()

            # ✅ Wait for place result to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "DUwDvf")))

            # ✅ Ensure the URL updates to a place page
            for _ in range(10):
                time.sleep(1)
                current_url = driver.current_url
                if "/place/" in current_url:
                    return current_url  # ✅ Capture final URL
            
        except (TimeoutException, NoSuchElementException, WebDriverException) as e:
            print(f"⚠️ Warning: Issue while searching {village_name} - {str(e)}")
            time.sleep(3)  # Wait before retrying

    return None  # Return None if all retries fail

def save_to_excel(village, url):
    """Save village, URL, latitude, and longitude to Excel immediately."""
    lat, lon = extract_lat_long(url) if url else (None, None)
    new_data = pd.DataFrame([{"Village": village, "Google Maps URL": url, "Latitude": lat, "Longitude": lon}])

    if os.path.exists(output_file):
        existing_data = pd.read_excel(output_file, engine="openpyxl")
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_df = new_data

    updated_df.to_excel(output_file, index=False, engine="openpyxl")

def main():
    for village in village_names:
        if village in processed_villages:
            print(f"⏭️ Skipping {village} (already processed)")
            continue

        print(f"🔍 Searching: {village}")
        url = search_village(village)

        if url:
            print(f"🌍 URL Found: {url}")
            save_to_excel(village, url)  # Save after every successful search
            processed_villages.add(village)  # Update processed set
        else:
            print(f"❌ No valid URL for {village}")

        time.sleep(2)  # Small delay before next search

    driver.quit()  # Close the browser
    print(f"✅ All URLs saved to {output_file}")

if __name__ == "__main__":
    main()
