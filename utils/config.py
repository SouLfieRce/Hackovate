import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Settings:
    """Application settings and constants (MySQL)."""

    # MySQL Database credentials
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASS: str = os.getenv("DB_PASS", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "bus_db")

    # SQLAlchemy connection string for MySQL
    SQLALCHEMY_DATABASE_URI: str = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # App constants
    APP_NAME: str = "Smart Bus Tracker"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")

    # Map settings
    DEFAULT_LAT: float = float(os.getenv("DEFAULT_LAT", 23.0225))
    DEFAULT_LON: float = float(os.getenv("DEFAULT_LON", 72.5714))
    DEFAULT_ZOOM: int = int(os.getenv("DEFAULT_ZOOM", 13))

settings = Settings()

# Example usage:
if __name__ == "__main__":
    print(f"Connecting to MySQL: {settings.SQLALCHEMY_DATABASE_URI}")
