from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Common placeholder patterns to detect (case-insensitive)
PLACEHOLDER_PATTERNS = [
    "your_password", "your-password", 
    "change-me", "change_me", 
    "placeholder", "password123",
    "example", "test123"
]

# Get DATABASE_URL from environment - no default with credentials for security
# Format: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please set it in your .env file with your actual PostgreSQL connection string. "
        "Example: postgresql+asyncpg://postgres:your_actual_password@localhost/loan_app_db"
    )

# Validate it's not a placeholder by checking for common placeholder patterns (case-insensitive)
url_lower = DATABASE_URL.lower()
if any(pattern in url_lower for pattern in PLACEHOLDER_PATTERNS):
    raise ValueError(
        "DATABASE_URL contains placeholder values. "
        "Please replace with your actual PostgreSQL credentials in the .env file. "
        "Example: postgresql+asyncpg://postgres:your_actual_password@localhost/loan_app_db"
    )

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
