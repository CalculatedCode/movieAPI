import requests
from bs4 import BeautifulSoup
import random

def scrape_quote(title):
    """Returns a random movie quote from a movie using the title (title should be exact)
    from moviequotes.com"""

    #Make request for search results from moviequotes.com
    url = 'https://www.moviequotes.com/search-quotes/?q='
    title_formatted = title.replace(' ', "+")
    url = url + title

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)


    #Validate response and process HTML
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        #get the quote text and the source (movie/tv show) for each entry on
        #search query page
        quotes = soup.find_all(class_="whole-read-more")
        sources = soup.find_all(class_="phrase-new-sources")

        #Function to format html leftovers (remove links and replace <br> with \n)
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

        #Function to remove extra text from "source" variable
        def clean_source(text):
            return text.replace("From the movie:", "").replace("From the TV Series:", "").replace("From the animation:", "").strip()

        #Pair each movie with a source
        pairs = [(get_formatted_text(q), clean_source(s.get_text(strip=True))) for q, s in zip(quotes, sources)]

        #Validate that the source part of the pair matches the title exactly (ignoring capitals)
        correct_pairs = []
        for pair in pairs:
            if pair[1].lower() == title.lower():
                correct_pairs.append(pair)

        #Select a random quote from the list of valid pairs or return "no quote found"
        try:
            selected_quote = random.choice(correct_pairs)[0]
        except IndexError:
            selected_quote = "no quote found"
        return selected_quote
    
    else:
        print(f"Failed to retrieve the page, status code: {response.status_code}")



