# 🛒 Amazon Product Scraper & Data Automation

This represents a robust Python automation tool designed to extract real-time product data from Amazon. It navigates through search pages, extracts key details, cleans the data, and exports it to a structured CSV/Excel file.

## 🚀 Key Features
- **Automated Browsing:** Uses `Selenium` to mimic human behavior and navigate multiple pages.
- **Data Extraction:** Scrapes Product Name, Live Price, Rating, and Product URL using `BeautifulSoup`.
- **Data Cleaning:** Uses `Pandas` to remove duplicates, fix currency symbols (PKR/USD), and handle missing values.
- **Anti-Detection:** Implements random delays to prevent IP blocking.
- **Export:** Saves valid data into a clean `CSV` file ready for analysis.

## 🛠️ Tech Stack
- **Language:** Python 3.13
- **Libraries:** Selenium, BeautifulSoup4, Pandas, Webdriver-Manager

## 📂 Output Sample
The script generates a clean CSV file like this:

| Name | Price | Rating | Product Link |
|------|-------|--------|--------------|
| Razer Viper V3 | 129.99 | 4.6 | https://amazon.com/... |
| Logitech G305 | 37.59 | 4.6 | https://amazon.com/... |

## ⚙️ How to Run

1. Install the required libraries:
   ```bash
   pip install -r requirements.txt
2. Run the script:
   python Amazon.py
