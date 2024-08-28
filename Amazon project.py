import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_amazon_product_links(category_url, max_items=100):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1"
    }
    
    product_links = []
    page = 1
    
    while len(product_links) < max_items:
        url = f"{category_url}&page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to retrieve page {page} for URL: {url} (Status Code: {response.status_code})")
            break
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if '/dp/' in href and href not in product_links:
                product_links.append("https://www.amazon.in" + href)
                if len(product_links) >= max_items:
                    break
        
        page += 1
        time.sleep(2)
    
    return product_links

def scrape_amazon_categories(categories):
    all_data = []

    for category_name, category_url in categories.items():
        print(f"Scraping category: {category_name}")
        product_links = get_amazon_product_links(category_url)
        if product_links:
            for link in product_links:
                all_data.append([category_name, link])
        else:
            print(f"No links retrieved for category: {category_name}")

    return all_data

categories = {
    "cribs": "https://www.amazon.com/cribs%2Caps%2C269&ref=nb_sb_ss_pltr-data-refreshed_2_5",
    "Gaming chair": "https://www.amazon.com/gaming+chair",
    "Gaming desktop": "https://www.amazon.com/gaming+desktop",
    "pet grooming": "https://www.amazon.in/s?k=pet+grooming&crid",
    "organic products": "https://www.amazon.in/s?k=organic+products&crid",
    "luggage tags": "https://https://www.amazon.in/s?k=luggage+tags",
    "Baby clothing": "https://https://www.amazon.in/s?k=babby+clothing",
    "Test and measurement equipment":"https://https://www.amazon.in/s?k=test+and+measurement+equipment"
   
}

data = scrape_amazon_categories(categories)

if data:
    df = pd.DataFrame(data, columns=["Category", "Product Link"])
    df.to_csv("amazon_product_links.csv", index=False)
    print("Scraping complete. Data saved to amazon_product_links.csv")
else:
    print("No data scraped, CSV file not created.")