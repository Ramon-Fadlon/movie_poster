import requests
import imdb
from config import TMDB_key

class TMDB:
    def __init__(self):
        self.key = TMDB_key

print(f'https://api.themoviedb.org/3/movie/550?api_key={TMDB_key}')

