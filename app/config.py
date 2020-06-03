class Config:
    MOVIE_API_BASE_URL = 'https://api.themoviedb.org/3/movie/{}?api_key={}'
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
