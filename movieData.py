import requests

def get_movie_id(movie_title, API_KEY, BASE_URL):

    search_url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": movie_title
    }
    
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        
        if results:
            first_movie = results[0]  # Take the first result as the most relevant
            return first_movie["id"], first_movie["title"], first_movie["release_date"]
        else:
            print("No movies found for the given title.")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    

    

def get_movie_data(movie_id, API_KEY, BASE_URL):
    movie_url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    response = requests.get(movie_url, params=params)

    if response.status_code == 200:
        data = response.json()
        title = data.get("title", "Unknown Title")
        overview = data.get("overview", "No description available.")
        poster_path = data.get("poster_path")

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            poster_url = "No poster available."

        return {"title": title, "overview": overview, "poster_url": poster_url}

    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

