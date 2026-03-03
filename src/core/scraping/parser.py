# LINK FOR SCRAPING: https://discord.com/api/v10/applications/detectable
import sqlite3 as sq
import requests as req
from loguru import logger
from pathlib import Path


DISCORD_API = "https://discord.com/api/v10/applications/detectable"
BASE_PATH = Path(__file__).resolve().parent
DB_PATH = BASE_PATH.parent / "database" / "games_info.db"


def fetch_games() -> list:
    response = req.get(DISCORD_API)
    if response.status_code != 200:
        logger.critical(f"Discord sent error! Status code: {response.status_code}")
        response.raise_for_status()
    data = response.json()
    logger.info(f"Fetched {len(data)} games")
    return data


def parse_game(app: dict) -> tuple:
    game_id = app["id"]
    game_name = app.get("name") or app["executables"][0]["name"].replace(".exe", "")
    return game_name, game_id


def sync_db(data: list, db_path=DB_PATH) -> int:
    db = sq.connect(db_path)
    cursor = db.cursor()
    cursor.execute("DELETE FROM games")
    for app in data:
        game_name, game_id = parse_game(app)
        cursor.execute(
            "INSERT OR IGNORE INTO games VALUES (?, ?)", (game_name, game_id)
        )
    db.commit()
    cursor.execute("SELECT COUNT(*) FROM games")
    total = cursor.fetchone()[0]
    db.close()
    logger.success(f"Synced {total} games to DB")
    return total


def sync_games(db_path: str = DB_PATH) -> None:
    data = fetch_games()
    total = sync_db(data, db_path)
    logger.info(f"Total in DB: {total}")


if __name__ == "__main__":
    sync_games()
