# Books-data-scraping


## Overview
This project involves scraping data like books name and their prices from the test website.

## Key Features
- Data extraction using Python
- Export to Excel
- Markdown documentation

***CODE ***
```
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define a single set of headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com",
    "Connection": "keep-alive"
}

url = "https://books.toscrape.com/catalogue/page-2.html"

# Make a request with the defined headers
response = requests.get(url, headers=headers)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')

# Extract and print book titles and prices
books = soup.find_all('article', class_='product_pod')

# Prepare a list to store the extracted data
data = []

for book in books:
    book_title = book.h3.a['title']
    book_price = book.find('p', class_='price_color').text
    data.append({"Title": book_title, "Price": book_price})

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file
df.to_excel("books.xlsx", index=False)

print("Data has been written to books.xlsx")
```
#   Conclusion
This project provides a foundational approach to web scraping with Python. By following the setup instructions and customizing the script, you can efficiently collect and analyze data from a variety of web sources.
