# LINK FOR SCRAPING: https://discord.com/api/v10/applications/detectable
import sqlite3 as sq
import requests as req

# from bs4 import BeautifulSoup   <- Black deleting this import as unused
from loguru import logger

# Request to link
paramaters = {"key1": "value1", "key2": "value2"}
response = req.get(
    "https://discord.com/api/v10/applications/detectable", params=paramaters
)

if response.status_code != 200:
    logger.critical(f"Discord sent error! Status code is: \n{response.status_code}")
    response.raise_for_status()


data = response.json()
print("Data type:", type(data))
print(len(data))
first_app = data[0]  # First detectable application
game_id = first_app["id"]
game_name = first_app.get("name") or first_app["executables"][0]["name"].replace(
    ".exe", ""
)
print(f"ID: {game_id}")
print(f"Game: {game_name}")


# Database interaction
db = sq.connect("../database/games_info.db")
cursor = db.cursor()

cursor.execute(
    """
    INSERT OR IGNORE INTO games VALUES (?, ?, ?)
    """,
    (game_name, game_id, 10),
)
db.commit()

cursor.execute(
    """
SELECT * FROM games
"""
)
print(cursor.fetchall())

db.close()
