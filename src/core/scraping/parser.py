# LINK FOR SCRAPING: https://discord.com/api/v10/applications/detectable
import sqlite3 as sq
import requests as req
from loguru import logger

# Request to link
response = req.get("https://discord.com/api/v10/applications/detectable")

if response.status_code != 200:
    logger.critical(f"Discord sent error! Status code is: \n{response.status_code}")
    response.raise_for_status()


data = response.json()
print("Data type:", type(data))
print(data.keys() if isinstance(data, dict) else data[:2])
print(f"Len of whole games list: {len(data)}")

# Database interaction
db = sq.connect("../database/games_info.db")
cursor = db.cursor()

cursor.execute("DELETE FROM games")
db.commit()

for app in data:
    game_id = app["id"]
    game_name = app.get("name") or app["executables"][0]["name"].replace(".exe", "")
    cursor.execute("INSERT OR IGNORE INTO games VALUES (?, ?)", (game_name, game_id))


db.commit()
print(f"Inserted {len(data)} games")

cursor.execute("SELECT COUNT(*) FROM games")
print(f"Total in DB: {cursor.fetchone()[0]}")

db.close()
