from bs4 import BeautifulSoup
import requests

def scrape_url_to_text(url: str) -> str:
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
    # url = 'https://brightdata.com/blog/how-tos/beautiful-soup-web-scraping'
    url = url

    page_html = get_page_contents(url)
    if not page_html:
        raise SystemExit("Failed to fetch page content")

    # 2. Parse the HTML content using BeautifulSoup
    # .content is preferred over .text for better character encoding handling
    soup = BeautifulSoup(page_html, 'html.parser')
    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        tag.decompose()
    main = soup.find('main') or soup.find('article') or soup.find(id='content')
    if main:
        soup = BeautifulSoup(str(main), 'html.parser')

    # 3. Extract plain text only (no HTML tags)
    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    plain_text = "\n".join(lines)

    return plain_text
    # 4. Save text to a file
    # with open("../output/scraped_page.txt", "w", encoding="utf-8") as f:
    #     f.write(plain_text)



