import os
import requests
import imdb
from config import TMDB_key

class tmdb_downloder:
    def __init__(self):
        self.Config_Pattern = 'http://api.themoviedb.org/3/configuration?api_key={key}'
        self.KEY = TMDB_key
        self.url = self.Config_Pattern.format(key=self.KEY)
        self.r = requests.get(self.url)
        self.config = self.r.json()
        self.secure_base_url = self.config['images']['secure_base_url']
        self.sizes = self.config['images']['poster_sizes']
        self.max_size = 'original'
        self.IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
        self.get_imdb_id()
        self.tmdb_posters()

    def get_imdb_id(self, title):
        ia = imdb.Cinemagoer()
        movies = ia.search_movie(title)
        imdbid = "tt" + movies[0].movieID
        self.tmdb_posters(title,imdbid)

    def tmdb_posters(self, title, count=None, outpath='.'):
        urls = get_poster_url(self.imdbid)
        if count is not None:
            urls = urls[:count]
        _download_image(title, urls, outpath)






