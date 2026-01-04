from bs4 import BeautifulSoup
import requests

# Function to get the HTML content of a page
def get_page_contents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        return page.content

    return None

# 1. URL of the page you want to scrape
url = 'https://brightdata.com/blog/how-tos/beautiful-soup-web-scraping'

page_html = get_page_contents(url)

# 2. Parse the HTML content using BeautifulSoup
# .content is preferred over .text for better character encoding handling
soup = BeautifulSoup(page_html, 'html.parser')
for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
    tag.decompose()
main = soup.find('main') or soup.find('article') or soup.find(id='content')
if main:
    soup = BeautifulSoup(str(main), 'html.parser')

# 3. Optional: Print the formatted HTML
# print(soup.prettify())

with open("../output/scraped_page.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())



