from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get DATABASE_URL from environment - no default with credentials for security
# Format: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please set it in your .env file with your actual PostgreSQL connection string. "
        "Example: postgresql+asyncpg://postgres:YOUR_ACTUAL_PASSWORD@localhost/loan_app_db"
    )

# Validate it's not a placeholder by checking for common placeholder patterns
placeholder_patterns = ["YOUR_PASSWORD", "your_password", "YOUR-PASSWORD", "CHANGE-ME", "PLACEHOLDER"]
if any(pattern in DATABASE_URL for pattern in placeholder_patterns):
    raise ValueError(
        "DATABASE_URL contains placeholder values. "
        "Please replace with your actual PostgreSQL credentials in the .env file. "
        "Example: postgresql+asyncpg://postgres:YOUR_ACTUAL_PASSWORD@localhost/loan_app_db"
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
