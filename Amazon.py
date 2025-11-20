import time
import random
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
SEARCH_QUERY = "gaming mouse"
PAGES_TO_SCRAPE = 2
OUTPUT_FILE = "amazon_final_clean.csv"

def get_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def clean_price(price_text):
        if not price_text:
            return "N/A"
    
    # Regex use kar ke sirf digits aur dot (.) ko rakho, baaqi sab ura do
        clean_val = re.sub(r'[^\d.]', '', price_text) 
    
        if clean_val:
            return clean_val
        return "N/A"

def scrape_amazon():
    driver = get_driver()
    all_products = []
    
    print(f"🚀 Starting Final Scraper for: '{SEARCH_QUERY}'...")

    for page in range(1, PAGES_TO_SCRAPE + 1):
        url = f"https://www.amazon.com/s?k={SEARCH_QUERY}&page={page}"
        print(f"📄 Scraping Page {page}...")
        
        driver.get(url)
        time.sleep(random.uniform(4, 7))
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        if not results:
            print("⚠️ No results found. Amazon might contain captcha.")
            break
            
        for item in results:
            try:
                # 1. TITLE
                title_tag = item.find("h2")
                title = title_tag.text.strip() if title_tag else "N/A"
                
                # 2. PRICE (Multi-check logic)
                price_text = ""
                # Check 1: Hidden price (common in listings)
                price_tag = item.find("span", class_="a-offscreen")
                if price_tag:
                    price_text = price_tag.text.strip()
                
                # Check 2: Visible price (if hidden is empty)
                if not price_text:
                    price_whole = item.find("span", class_="a-price-whole")
                    if price_whole:
                        price_text = price_whole.text.strip()
                        price_fraction = item.find("span", class_="a-price-fraction")
                        if price_fraction:
                            price_text += "." + price_fraction.text.strip()

                # Clean the messy PKR/Symbol string
                final_price = clean_price(price_text)

                # 3. RATING
                rating_tag = item.find("span", class_="a-icon-alt")
                rating = rating_tag.text.split(" ")[0] if rating_tag else "N/A"
                
                # 4. LINK
                link_tag = item.find("a", class_="a-link-normal s-no-outline")
                link = "https://www.amazon.com" + link_tag['href'] if link_tag else "N/A"
                
                # Sirf wo save karo jinka data meaningful ho
                if final_price != "N/A":
                    all_products.append({
                        "Name": title,
                        "Price": final_price,
                        "Rating": rating,
                        "Product Link": link
                    })
                
            except Exception:
                continue

        print(f"✅ Page {page} done. Total items: {len(all_products)}")

    driver.quit()
    
    # --- SAVE WITH UTF-8-SIG (Fixes Excel Symbols) ---
    if all_products:
        df = pd.DataFrame(all_products)
        # Saving with utf-8-sig fixes the weird characters in Excel
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"\n🎉 Data Saved to '{OUTPUT_FILE}' cleanly!")
        print(df.head())
    else:
        print("\n❌ No valid data found.")

if __name__ == "__main__":
    scrape_amazon()