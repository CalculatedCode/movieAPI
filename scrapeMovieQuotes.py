import requests
from bs4 import BeautifulSoup
import random

def scrape_quote(title):
    
    url = 'https://www.moviequotes.com/search-quotes/?q='
    title_formatted = title.replace(' ', "+")
    url = url + title

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")


        quotes = soup.find_all(class_="whole-read-more")
        sources = soup.find_all(class_="phrase-new-sources")


        def get_formatted_text(element):
            text_parts = []
            for child in element.contents:
                if isinstance(child, str):
                    text_parts.append(child.strip())
                elif child.name == "a": 
                    text_parts.append(f' {child.get_text(strip=True)} ')
                elif child.name == "br":
                    text_parts.append("\n")
            return " ".join(text_parts).replace("  ", " ") 


        def clean_source(text):
            return text.replace("From the movie:", "").replace("From the TV Series:", "").replace("From the animation:", "").strip()

        pairs = [(get_formatted_text(q), clean_source(s.get_text(strip=True))) for q, s in zip(quotes, sources)]


        correct_pairs = []

        for pair in pairs:
            if pair[1].lower() == title.lower():
                correct_pairs.append(pair)

        try:
            selected_quote = random.choice(correct_pairs)[0]
        except IndexError:
            selected_quote = "no quote found"
        return selected_quote
    
    else:
        print(f"Failed to retrieve the page, status code: {response.status_code}")



#drop punctuation and unimportant words for comparison [the, a, of, etc]