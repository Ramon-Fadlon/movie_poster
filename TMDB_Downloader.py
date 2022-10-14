import requests
import imdb
from config import TMDB_key

class TMDB:
    def __init__(self):
        self.KEY = TMDB_key
        self.movieID = ""


    def get_imdb_id(self, title):
        ia = imdb.Cinemagoer()
        movies = ia.search_movie(title)
        print(movies[0].movieID)
        return self.movieID == movies[0].movieID

    def get_image_config(self):
        CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'

        url = CONFIG_PATTERN.format(key=self.KEY)
        r = requests.get(url)
        config = r.json()
        base_url = config["images"]["base_url"]
        poster_sizes = config["images"]["poster_sizes"]
        return base_url, poster_sizes

    def get_image(self, title):
        id = self.get_imdb_id(title)
        if id == "null":
            print("there is no such movie")
        else:
            IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
            r = requests.get(IMG_PATTERN.format(key=self.KEY, imdbid=id))
            api_response = r.json()
            posters = api_response['posters']
            print(posters)


# print(f'https://api.themoviedb.org/3/movie/550?api_key={TMDB_key}')
new_search = TMDB()
new_search.get_imdb_id("Women")
new_search.get_image_config()

