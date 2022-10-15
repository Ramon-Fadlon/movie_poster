# import requests
# import imdb
# from config import TMDB_key
#
# class TMDB:
#     def __init__(self):
#         self.KEY = TMDB_key
#         self.movieID = ""
#
#
#     def get_imdb_id(self, title):
#         ia = imdb.Cinemagoer()
#         movies = ia.search_movie(title)
#         print(movies[0].movieID)
#         return self.movieID == movies[0].movieID
#
#     def get_image_config(self):
#         CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
#
#         url = CONFIG_PATTERN.format(key=self.KEY)
#         r = requests.get(url)
#         config = r.json()
#         base_url = config["images"]["base_url"]
#         poster_sizes = config["images"]["poster_sizes"]
#         return base_url, poster_sizes
#
#     def get_image(self, title):
#         id = self.get_imdb_id(title)
#         if id == "null":
#             print("there is no such movie")
#         else:
#             IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
#             r = requests.get(IMG_PATTERN.format(key=self.KEY, imdbid=id))
#             api_response = r.json()
#             posters = api_response['posters']
#             print(posters)
#
#
# # print(f'https://api.themoviedb.org/3/movie/550?api_key={TMDB_key}')
# new_search = TMDB()
# new_search.get_imdb_id("Women")
# new_search.get_image_config()
import os
import requests
import imdb
CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
KEY =  'a1f38ebcb3d2bfe7608f1bfe2dcdd10d'


def _get_json(url):
    r = requests.get(url)
    return r.json()

def get_imdb_id(title):
    ia = imdb.Cinemagoer()
    movies = ia.search_movie(title)
    imdbid = "tt" + movies[0].movieID
    tmdb_posters(title,imdbid)


def _download_image(title,urls, path='.'):
    """download all images in list 'urls' to 'path' """

    r = requests.get(urls[0])
    filetype = r.headers['content-type'].split('/')[-1]
    filename = '{0}.{1}'.format( title,filetype)
    filepath = os.path.join(path, filename)
    with open(filepath, 'wb') as w:
        w.write(r.content)


def get_poster_url(imdbid):
    """ return image urls of posters for IMDB id
        returns all poster images from 'themoviedb.org'. Uses the
        maximum available size.
        Args:
            imdbid (str): IMDB id of the movie
        Returns:
            list: list of urls to the images
    """
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']

    """
        'sizes' should be sorted in ascending order, so
            max_size = sizes[-1]
        should get the largest size as well.        
    """

    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])

    max_size = max(sizes, key=size_str_to_int)

    posters = _get_json(IMG_PATTERN.format(key=KEY, imdbid=imdbid))['posters']
    poster_urls = []
    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, max_size, rel_path)
        poster_urls.append(url)

    return poster_urls


def tmdb_posters(title,imdbid, count=None, outpath='.'):
    urls = get_poster_url(imdbid)
    if count is not None:
        urls = urls[:count]
    _download_image(title,urls, outpath)


if __name__ == "__main__":
    get_imdb_id("spiderman3")
