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
    if not isinstance(app, dict):
        logger.warning(f"Skipping non-dict app: {app!r}")
        return None, None

    game_id = app.get("id")
    if not game_id:
        logger.warning(f"Skipping app without id: {app}")
        return None, None

    game_name = app.get("name")
    if not game_name:
        if app.get("executables") and app["executables"]:
            game_name = app["executables"][0]["name"].replace(".exe", "")
        else:
            logger.warning(f"Skipping app without name or executables: {app}")
            return None, None

    return game_name, game_id


def sync_db(data: list, db_path=DB_PATH) -> int:
    db = sq.connect(db_path)
    cursor = db.cursor()
    cursor.execute("DELETE FROM games")

    synced = 0
    for app in data:
        game_name, game_id = parse_game(app)
        if game_name is None or game_id is None:
            continue

        cursor.execute(
            "INSERT OR IGNORE INTO games VALUES (?, ?)", (game_name, game_id)
        )
        synced += 1

    db.commit()
    cursor.execute("SELECT COUNT(*) FROM games")
    total = cursor.fetchone()[0]
    db.close()
    logger.success(f"Synced {synced} games to DB (total in DB: {total})")
    return total


def find_games_by_name(name: str, db_path=DB_PATH) -> list[tuple[str, str]]:
    db = sq.connect(db_path)
    cursor = db.cursor()
    cursor.execute(
        "SELECT game_name, game_rpc_id FROM games WHERE game_name LIKE ? ORDER BY game_name",
        (f"%{name}%",),
    )
    matches = cursor.fetchall()
    db.close()
    return matches
