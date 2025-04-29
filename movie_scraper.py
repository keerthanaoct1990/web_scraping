import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_imdb_top_movies():
    url = "https://www.imdb.com/chart/top"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = []

    ul_block = soup.select_one('ul.ipc-metadata-list')
    if ul_block:
        li_blocks = ul_block.find_all('div', class_="ipc-metadata-list-summary-item__c") 
        for li in li_blocks:
            title = li.find('h3', class_="ipc-title__text").text
            full_title = title.strip()

            # Remove "1. " or "2. " using split
            if '. ' in full_title:
                movie_name = full_title.split('. ', 1)[1]
            else:
                movie_name = full_title

            year = li.find('span', class_="sc-5179a348-7 idrYgr cli-title-metadata-item").text
            rating = li.find('span', class_="ipc-rating-star--rating").text

            movies.append((movie_name, year, float(rating)))

    df = pd.DataFrame(movies, columns=["Movie", "Year", "Rating"])
    return df

#save to csv file
def save_to_csv(df, filename="imdb_top_movies.csv"):
    df.to_csv(filename, index=False)
    print(f"Saved to {filename}")

def search_movie(df, query):
    result = df[df['Movie'].str.contains(query, case=False, na=False)]
    if result.empty:
        print("No matching movie found.")
    else:
        print(result)

def show_top_n(df, n=10):
    print(df.head(n))


df = scrape_imdb_top_movies()
save_to_csv(df)
show_top_n(df, 10)     
search_movie(df, "Inception") 
