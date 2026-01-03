# LINK FOR SCRAPING: https://discord.com/api/v10/applications/detectable
import sqlite3 as sq
import requests as req

# from bs4 import BeautifulSoup   <- Black deleting this import as unused
from loguru import logger

# Request to link
response = req.get("https://discord.com/api/v10/applications/detectable")

if response.status_code != 200:
    logger.critical(f"Discord sent error! Status code is: \n{response.status_code}")
    response.raise_for_status()


data = response.json()
print("Data type:", type(data))
# logger.success(response.json())


db = sq.connect("../database/games_info.db")
cursor = db.cursor()

cursor.execute(
    """
    INSERT OR IGNORE INTO games VALUES (?, ?, ?)
    """,
    ("test", "123", 15),
)
db.commit()

cursor.execute(
    """
SELECT * FROM games
"""
)
print(cursor.fetchall())

db.close()
