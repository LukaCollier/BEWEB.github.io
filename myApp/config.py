ENV="development"
DEBUG=True
SEND_FILE_MAX_AGE_DEFAULT = 0
SECRET_KEY ="pouletteetpoulet"

WEB_SERVER={
    "host": "localhost",
    "port":8080,
}

DB_SERVER={
    "user":"root",
    "password":"mysql",
    "host":"localhost",
    "port": 3306,
    "database": "ienac25_flashcards_groupea",
    "raise_on_warnings": True
}
