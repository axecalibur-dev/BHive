from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch PostgreSQL credentials from environment variables
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Define the database connection URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the async engine for SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# SessionLocal for creating sessions to interact with the database
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Initialize FastAPI app
app = FastAPI()

# Test the connection by executing a simple query (SELECT 1)
async def init_db():
    try:
        async with SessionLocal() as session:
            result = await session.execute(select(1))
            print(result.scalar(), flush=True)  # Use `scalar()` to get the result of a simple query

        logging.info("Database connected successfully")
        print("Database connected", flush=True)

    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        print("Database connection failed", flush=True)

# Close the connection
async def close_db():
    try:
        await engine.dispose()  # Disposes the engine and connections
        logging.info("Database connections closed")
    except Exception as e:
        logging.error(f"Error closing database connections: {e}")
        print("Error closing database connections", flush=True)

# Async context manager to handle database sessions
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session  # FastAPI will handle this as a dependency
 # Yield the session object (AsyncSession)
# FastAPI event to initialize the database connection on startup
@app.on_event("startup")
async def startup():
    await init_db()

# FastAPI event to close the database connection on shutdown
@app.on_event("shutdown")
async def shutdown():
    await close_db()
