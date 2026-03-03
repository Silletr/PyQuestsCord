from core.scraping.parser import sync_games
from loguru import logger


def main():
    logger.info("Starting scraping")
    sync_games()
    logger.success("Successfully ended scraping, all games in on core/database/")


if __name__ == "__main__":
    main()
