import requests
from bs4 import BeautifulSoup
import json
import os

# Get the current directory and the root directory (one level up)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)  # This gets the parent directory

BASE_URL = "https://www.constitutionofindia.net"

# List of Roman numerals for parts (I to XXII)
roman_parts = [
    "i", "ii", "iii", "iv", "iva", "v", "vi", "vii", "viii", "ix", "ixa", "ixb", "x",
    "xi", "xii", "xiii", "xiv", "xiva", "xv", "xvi", "xvii", "xviii", 
    "xix", "xx", "xxi", "xxii"
]

def get_all_article_urls():
    article_urls = {}

    for part in roman_parts:
        part_url = f"{BASE_URL}/parts/part-{part}/"
        response = requests.get(part_url)

        if response.status_code != 200:
            print(f"Failed to fetch Part {part.upper()}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        article_links = soup.find_all('a', class_='no-underline text-inherit')

        part_articles = []
        for link in article_links:
            href = link['href']
            if not href.startswith('http'):
                href = BASE_URL + href
            part_articles.append(href)

        article_urls[f"Part {part.upper()}"] = part_articles

    return article_urls

def extract_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').text.strip()
    content_div = soup.find('div', class_='article-detail__content__sub-block')
    content = content_div.text.strip() if content_div else 'Content not found'

    versions = {}
    version_blocks = soup.find_all('div', class_='article-detail__content__main-block')

    if version_blocks:
        for idx, block in enumerate(version_blocks[:-1]):
            version_title = f"Version {idx + 1}"
            versions[version_title] = block.text.strip() if block else 'Version content not found'

        summary_block = version_blocks[-1]
        summary_text = summary_block.text.strip()

        if "Summary" in summary_text or "Draft Article" in summary_text:
            summary = summary_text
        else:
            versions[f"Version {len(version_blocks)}"] = summary_text
            summary = "Summary not found"
    else:
        summary = "Summary not found"

    return {
        'title': title,
        'content': content,
        'versions': versions,
        'summary': summary,
        'url': url
    }

def scrape_all_articles():
    all_articles = get_all_article_urls()
    structured_data = {}

    for part, links in all_articles.items():
        structured_data[part] = []  # Create a list for each part
        for link in links:
            article_data = extract_article(link)
            if article_data:
                structured_data[part].append(article_data)

    # Create the output file path in the root directory
    output_file = os.path.join(root_dir, 'constitution_articles_by_parts.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, ensure_ascii=False, indent=4)

    print(f"Extraction complete! Data saved to '{output_file}'.")

# Run the complete scraper
scrape_all_articles()