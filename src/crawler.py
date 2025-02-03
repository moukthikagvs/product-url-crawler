 import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# domains that require selenium
selenium_domains = {"croma.com", "ajio.com", "tatacliq.com", "reliancedigital.in", "shopclues.com"}

domains = {
    "amazon.in": "https://www.amazon.in/s?k={category}",
    "flipkart.com": "https://www.flipkart.com/search?q={category}",
    "tatacliq.com": "https://www.tatacliq.com/search/?searchCategory=all&text={category}",
    "reliancedigital.in": "https://www.reliancedigital.in/search?q={category}:relevance",
    "croma.com": "https://www.croma.com/searchB?q={category}",
    "snapdeal.com": "https://www.snapdeal.com/search?keyword={category}",
    "ajio.com": "https://www.ajio.com/search/?text={category}",
    "paytmmall.com": "https://paytmmall.com/shop/search?q={category}",
    "shopclues.com": "https://www.shopclues.com/search?q={category}"
}

categories = ["smart phones", "smart watches", "laptop bags"]

product_patterns = {
    "amazon.in": "/dp/",
    "flipkart.com": "/p/",
    "tatacliq.com": "/product/",
    "reliancedigital.in": "/p/",
    "croma.com": "/p/",
    "snapdeal.com": "/product/",
    "ajio.com": "/p/",
    "paytmmall.com": "/p/",
    "shopclues.com": "/product/"
}

#user agent rotation 
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

# set up selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_product_links(domain, category):
    """Fetch product links from a given domain and category"""
    search_url = domains[domain].format(category=category)
    product_links = set()  # Using set to avoid duplicates

    headers = {"User-Agent": random.choice(user_agents), "Accept-Language": "en-US,en;q=0.9"}

    if domain in selenium_domains:
        print(f" Using Selenium for {domain}")
        try:
            driver.get(search_url)
            time.sleep(random.uniform(3, 6))
            soup = BeautifulSoup(driver.page_source, "html.parser")
        except Exception as e:
            print(f" Selenium failed for {search_url}: {e}")
            return []
    else:
        print(f" Using requests for {domain}")
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f" Requests failed for {search_url}: {e}")
            return []

    # Extract links
    for a in soup.find_all("a", href=True):
        link = urljoin(search_url, a["href"])
        if product_patterns.get(domain, "") in link:
            product_links.add(link)

    print(f" Found {len(product_links)} product links for {category} on {domain}")
    return list(product_links)  # Convert set back to list

def save_to_csv(product_urls):
    """Save product URLs to a CSV file"""
    rows = [[domain, category, url] for domain, categories in product_urls.items() for category, urls in categories.items() for url in urls]

    df = pd.DataFrame(rows, columns=["Domain", "Category", "Product URL"])
    csv_path = "C:/Users/moukt/OneDrive/Desktop/product_urls.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n CSV file saved to {csv_path}")

def main():
    product_urls = {} # empty dictionary to store scraped product urls

    for category in categories:
        print(f"\n Scraping category: {category.upper()}")

        for domain in domains:
            product_urls.setdefault(domain, {})  # Avoid unnecessary condition check
            product_urls[domain][category] = get_product_links(domain, category)

    #  To save results in JSON format
    json_path = "C:/Users/moukt/OneDrive/Desktop/product_urls.json"
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(product_urls, file, indent=4)
    print(f"\n JSON file saved to {json_path}")

    # To save results in CSV format
    save_to_csv(product_urls)

    driver.quit()  # Close Selenium

if __name__ == "__main__":
    main()

