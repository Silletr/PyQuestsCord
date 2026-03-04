from core.scraping.parser import sync_db, find_games_by_name, fetch_games
from loguru import logger


def main():
    logger.info("Starting scraping")
    data = fetch_games()
    sync_db(data)
    logger.success("Successfully ended scraping, all games in on core/database/")
    print("---" * 5)
    game = input("Write game name: \n")
    if game:
        game_id = find_games_by_name(game)
        if game_id:
            print(f"Found: {game} → ID: {game_id}")

    else:
        print(f"No game found matching '{game}'")


if __name__ == "__main__":
    main()
