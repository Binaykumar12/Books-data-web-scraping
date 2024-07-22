import requests
from bs4 import BeautifulSoup

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

# Extract the title of the page


# Extract and print book titles and prices
books = soup.find_all('article', class_='product_pod')
for book in books:
    book_title = book.h3.a['title']
    book_price = book.find('p', class_='price_color').text
    print(f"Title: {book_title}, Price: {book_price}")