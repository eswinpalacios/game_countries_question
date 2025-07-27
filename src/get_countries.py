import json
import os
import time
from typing import List, Dict, Any
import requests

# Constants
COUNTRIES_API = "https://restcountries.com/v3.1/all?fields=name,capital,currencies,languages,region,subregion"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "countries.json")

def fetch_countries_data() -> List[Dict[str, Any]]:
    """Fetch countries data from the REST Countries API with retry logic."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")
            response = requests.get(
                COUNTRIES_API,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print("All attempts failed.")
                return []
            time.sleep(1)  # Wait before retry
    return []

def filter_american_countries(countries_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter countries to include only those from the Americas."""
    return [country for country in countries_data if country.get("region") == "Americas"]

def process_country_data(country_data: Dict[str, Any]) -> Dict[str, str]:
    """Process raw country data to extract required fields."""
    return {
        "name": country_data.get("name", {}).get("common", ""),
        "capital": country_data.get("capital", [""])[0] if country_data.get("capital") else "",
        "currency": next(iter(country_data.get("currencies", {}).values()), {}).get("name", ""),
        "language": next(iter(country_data.get("languages", {}).values()), ""),
        "region": country_data.get("region", ""),
        "subregion": country_data.get("subregion", "")
    }

def save_countries_data(countries: List[Dict[str, str]]) -> None:
    """Save processed countries data to a JSON file."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(countries, f, ensure_ascii=False, indent=2)

def main():
    print("Fetching countries data...")
    countries_data = fetch_countries_data()
    
    if not countries_data:
        print("No data received. Exiting...")
        return
    
    print(f"Filtering American countries...")
    american_countries = filter_american_countries(countries_data)
    
    print(f"Processing {len(american_countries)} American countries...")
    processed_countries = [process_country_data(country) for country in american_countries]
    
    print(f"Saving data to {OUTPUT_FILE}...")
    save_countries_data(processed_countries)
    print(f"Done! Saved {len(processed_countries)} American countries.")

if __name__ == "__main__":
    main()
