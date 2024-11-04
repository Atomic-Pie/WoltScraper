# Wolt Scraper and Categorizer

A fast and simple web scraper for Wolt (a food app in Hungary) that collects menu data for a given address and categorizes it into an Excel file. This tool scrapes the site’s HTML, extracts the menu items, and organizes them by category and subcategory in a user-friendly format.

## How It Works

The scraper pulls menu data from Wolt's site for any specified address and formats it in an Excel file. This is ideal for quick data collection, browsing menus, or analyzing food options in a particular area.

## Instructions

1. **Get the HTML:**
   - Go to [Wolt Restaurants](https://wolt.com/en/discovery/restaurants?sorting=distance).
   - Enter your address to display nearby restaurants.
   - Open Developer Tools (press `F12`) and copy the entire HTML source code.

2. **Save the HTML:**
   - Paste the copied HTML into a file named `wolt.txt` in your working directory.

3. **Run the Scraper and Categorizer:**
   - Run `scraper.py` to extract menu data.
   - Run `categorize.py` to organize items by category and subcategory.

4. **Get Results:**
   - The final output, `menu_categorized_with_subcategories.xlsx`, will contain all available menu items organized in an easy-to-navigate Excel sheet.

### Program Descriptions

1. **scraper.py**
   - **Purpose**: This script extracts menu data from Wolt's site. It performs two main tasks: first, it collects restaurant names and URLs from a local HTML file (`wolt.txt`), then it scrapes each restaurant's menu for items, descriptions, and prices.
   - **Output Files**:
     - `wolt_links.xlsx`: Contains a list of restaurant names and URLs.
     - `menu_scraped.xlsx`: Compiles menu items from all restaurants into a single file with columns for Store Name, Item, Description, and Price.

2. **categorize.py**
   - **Purpose**: This script categorizes the scraped menu items from `menu_scraped.xlsx` based on keywords for various categories and subcategories (such as "Burger Types" or "Pasta and Noodles"). It appends each item with its assigned category and subcategory.
   - **Output File**:
     - `menu_categorized_with_subcategories.xlsx`: An organized Excel file where each menu item is assigned to a main category and subcategory, making it easy to analyze food types.

