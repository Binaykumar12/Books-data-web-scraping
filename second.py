import requests
import random
from bs4 import BeautifulSoup
import time
import pandas as pd

# Defining the headers for HTTP requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept-Language': 'en-US, en;q=0.5'
}

# Function to get the links from the main search page
def get_product_links(soup):
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list = [link.get('href') for link in links if 'charge' not in link.get('href')]
    return links_list

# Function to fetch and parse product details from each link
def get_product_details(link):
    retries = 3
    for _ in range(retries):
        try:
            new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Extracting title
            title = new_soup.find("span", attrs={"id": "productTitle"})
            title_text = title.text.strip() if title else "N/A"

            # Extracting brand
            brand = new_soup.find("tr", attrs={"class": "po-brand"})
            brand_name = brand.find("span", attrs={"class": "po-break-word"}).text.strip() if brand else "N/A"

            # Extracting price
            price = new_soup.find("span", attrs={"class": "a-price"})
            actual_price = price.find("span", attrs={"class": "a-offscreen"}) if price else None
            price_text = actual_price.text.strip() if actual_price else "N/A"

            # Extracting rating
            rating = new_soup.find("i", attrs={"class": "a-icon-star"})
            rating_statement = rating.find("span", attrs={"class": "a-icon-alt"}) if rating else None
            rating_text = rating_statement.text.strip() if rating_statement else "N/A"

            # Extracting Maximum Display Resolution
            maximum_display_resolution = new_soup.find("tr", attrs={"class":"po-display.resolution_maximum"})
            maximum_display_resolution_name = maximum_display_resolution.find("span", attrs={"class": "po-break-word"}).text.strip() if maximum_display_resolution else "N/A"

            # Extracting Memory Storage capacity
            memory_storage = new_soup.find("tr", attrs={"class":"po-memory_storage_capacity"})
            actual_storage = memory_storage.find("span", attrs={"class": "po-break-word"}).text.strip() if memory_storage else 'N/A'

            # Extracting Screen Size
            screen = new_soup.find("tr", attrs={"class":"po-display.size"})
            screen_size = screen.find("span", attrs={"class": "po-break-word"}).text.strip() if screen else 'N/A'

            # Extracting Model Name
            model = new_soup.find("tr", attrs={"class":"po-model_name"})
            model_name = model.find("span", attrs={"class": "po-break-word"}).text.strip() if model else 'N/A'

            return {
                "Brand": brand_name,
                "Title": title_text,
                "Price": price_text,
                "Rating": rating_text,
                "maximum_display_resolution": maximum_display_resolution_name,
                "Memory": actual_storage,
                "Screen": screen_size,
                "Model": model_name
            }
        except requests.exceptions.RequestException as e:
            print(f"Request failed for link: https://www.amazon.com{link} - {e}")
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"Error processing link: https://www.amazon.com{link} - {e}")
            return None
    return None

# List to store product details
products = []

# Loop through the first 20 pages
for page in range(1, 21):
    # Sending an HTTP request to the Amazon webpage
    URL = f"https://www.amazon.com/s?k=ipads&page={page}"
    webpage = requests.get(URL, headers=HEADERS)

    # Creating a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Extracting links
    product_links = get_product_links(soup)

    # Looping over the extracted links
    for index, link in enumerate(product_links):
        details = get_product_details(link)
        if details:
            products.append(details)
            print(f"+--------------------\n|{page}.{index + 1} Product Details:\n|Brand: {details['Brand']}\n|Title: {details['Title']}\n|Price: {details['Price']}\n|Rating: {details['Rating']}\n|Display Resolution (Maximum): {details['maximum_display_resolution']}\n|Memory Storage Capacity: {details['Memory']}\n|Screen Size: {details['Screen']}\n|Model Name: {details['Model']}\n_+_+_+_+_+_+_+_+_+\n")
        # Adding a delay to avoid getting blocked
        time.sleep(random.uniform(1, 3))

# Creating a DataFrame from the product list
df = pd.DataFrame(products)

# Saving the DataFrame to a CSV file
df.to_csv('v2_amazon_ipads.csv', index=False)

print(f"Details of {len(products)} products saved to v2_amazon_ipads.csv")