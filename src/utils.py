TYPE_DATA = {
    "TV Series": "TV Series",
    "TV Movie": "TV Movie",
    "TV Mini-Series": "TV Mini-Series",
    "Video game released": "Video game",
    "Episode": "Episode",
}

CURRENCY_VALUES = {
    "GBP": 1.30,
    "EUR": 1.18,
    "AUD": 0.73,
    "THB": 0.032,
    "KRW": 0.00084,
    "NOK": 0.11,
    "FRF": 0.18,
    "INR": 0.014,
    "HKD": 0.13,
    "DKK": 0.16,
    "JPY": 0.0094,
    "ESP": 1.18,
    "CAD": 0.76,
    "$": 1,
}

FIELDS = [
    ("movie_title", "Title"),
    ("director", "Director"),
    ("stars", "Actor"),
    ("genres", "Genre"),
]

COLUMNS = [
    ("index", "Default"),
    ("title_year", "Year"),
    ("movie_title", "Title"),
    ("imdb_score", "IMDB Score"),
]

ORDER = [
    ("asc", "Ascending"),
    ("desc", "Descending"),
]
