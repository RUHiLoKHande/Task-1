import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for tag in soup(['sup', 'style', 'script', 'table', 'figure']):
        tag.decompose()

    text = soup.get_text(separator='\n')
    clean_lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(clean_lines)
