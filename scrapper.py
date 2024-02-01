import requests
from bs4 import BeautifulSoup
import csv

# Amazon search URL
# URL you are scraping
url = 'https://www.example.in/s?k=PS5+games'

# Headers observed from Postman
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; your-browser-info)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
}

# Send the request with the headers
response = requests.get(url, headers=headers)

print(response)
# Parse HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Find product elements
products = soup.find_all('div', {'data-component-type': 's-search-result'})

# CSV file setup
csv_file = open('output.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Image', 'Name', 'Brand', 'Price'])

# Extract data and write to CSV
for product in products:
    # Extracting image URL
    image = product.find('img', {'class': 's-image'})['src']

    # Extracting name
    name = product.find('h2').get_text(strip=True)

    # Extracting brand and price
    brand_price_div = product.find('div', {'data-cy': 'price-recipe'})
    brand = brand_price_div.find('a').get_text(strip=True) if brand_price_div else 'N/A'
    # Extracting price
    price_div = product.find('span', {'class': 'a-price'})  # Update class as per current structure
    price = price_div.get_text(strip=True) if price_div else 'N/A'

    # Writing to CSV
    csv_writer.writerow([image, name, brand, price])
    print(name, brand, price)

csv_file.close()
