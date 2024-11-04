import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Extract Store Names and URLs from wolt.txt
def extract_store_links(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    store_names, urls = [], []
    
    # Locate each restaurant element
    for restaurant in soup.select('.sc-acb291ec-0.ejIrBA a'):
        url = restaurant.get('href')
        name_tag = restaurant.find_next('h3')  # Locate the h3 tag for the name
        name = name_tag.get_text(strip=True) if name_tag else "Unknown Store"
        
        if name and url:
            store_names.append(name)
            urls.append("https://wolt.com" + url)
    
    # Save to Excel
    df_links = pd.DataFrame({
        'Store Name': store_names,
        'URL': urls
    })
    df_links.to_excel('wolt_links.xlsx', index=False)

# Step 2: Scrape menu items from each URL
def scrape_menu(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    items, descriptions, prices = [], [], []
    
    # Loop through each menu item
    for item in soup.select('[data-test-id="horizontal-item-card"]'):
        item_name = item.find("h3", {"data-test-id": "horizontal-item-card-header"})
        item_description = item.find("p", {"class": "du2tpot"})
        item_price = item.find("span", {"data-test-id": "horizontal-item-card-price"})

        if item_name:
            items.append(item_name.get_text(strip=True))
        else:
            items.append("")
        
        if item_description:
            descriptions.append(item_description.get_text(strip=True))
        else:
            descriptions.append("")
        
        if item_price:
            prices.append(item_price.get_text(strip=True))
        else:
            prices.append("")
    
    return items, descriptions, prices

# Step 3: Compile all menus into one Excel file
def compile_menus(input_file):
    df_links = pd.read_excel(input_file)
    store_names, items, descriptions, prices = [], [], [], []
    
    for _, row in df_links.iterrows():
        store_name = row['Store Name']
        url = row['URL']
        
        # Scrape each menu
        menu_items, menu_descriptions, menu_prices = scrape_menu(url)
        
        # Append data to master lists
        store_names.extend([store_name] * len(menu_items))
        items.extend(menu_items)
        descriptions.extend(menu_descriptions)
        prices.extend(menu_prices)
    
    # Save compiled data to Excel
    df_menu = pd.DataFrame({
        'Store Name': store_names,
        'Item': items,
        'Description': descriptions,
        'Price': prices
    })
    df_menu.to_excel('menu_scraped.xlsx', index=False)

# Execute the functions
extract_store_links('wolt.txt')    # Extract store names and URLs to wolt_links.xlsx
compile_menus('wolt_links.xlsx')   # Compile menus into menu_scraped.xlsx
