import logging
import os
import sys
from alembic.config import Config
from alembic import command
from alembic.util.exc import CommandError
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings

# Add the current directory to the sys.path so that the 'app' module can be found
sys.path.append(os.getcwd())

logger = logging.getLogger(__name__)


def run_migrations():
    """Run database migrations using Alembic."""
    logger.info("Running database migrations...")

    # Path to the alembic.ini file
    alembic_cfg = Config("alembic.ini")

    # Override the sqlalchemy.url in alembic.ini with the environment variable
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    try:
        # Run the 'upgrade head' command
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully.")
    except (CommandError, SQLAlchemyError) as e:
        logger.error(f"Error running database migrations: {e}")
        # In a real production environment, you might want to exit here
        # raise e


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    run_migrations()
