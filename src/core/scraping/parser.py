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
        logger.critical(f"Discord sent error! Status code: {
                        response.status_code}")
        response.raise_for_status()
    data = response.json()
    logger.info(f"Fetched {len(data)} games")
    return data


def parse_game(app: dict) -> tuple:
    game_name = app.get("name", "Unknown")

    executables = app.get("executables", [])
    if not executables:
        return game_name, "no_executables"

    first_exec = executables[0]
    game_executable = first_exec.get(
        "name", "unknown") if first_exec else "no_name"

    return game_name or game_executable.replace(".exe", ""), game_executable


def sync_db(data: list, db_path=DB_PATH) -> int:
    db = sq.connect(db_path)
    cursor = db.cursor()
    cursor.execute("DELETE FROM games")

    synced = 0
    for app in data:
        game_name, game_id = parse_game(app)
        if game_name is None or game_id is None:
            continue

        game_name, game_executable = parse_game(app)
        cursor.execute(
            "INSERT OR IGNORE INTO games VALUES (?, ?)", (
                game_name, game_executable)
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


def sync_games(db_path=DB_PATH) -> None:
    data = fetch_games()
    total = sync_db(data, db_path)
    logger.info(f"Total in DB: {total}")


if __name__ == "__main__":
    sync_games()
