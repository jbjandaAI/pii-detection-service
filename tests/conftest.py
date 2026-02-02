import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.infra.database import Base, DATABASE_URL

# Use the environment variable or default to localhost
# In a real CI, this might point to a service like 'postgres-test'
TEST_DATABASE_URL = DATABASE_URL

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    Creates a fresh SQLAlchemy Session for a test.
    Rolls back the transaction after the test is done to keep the DB clean.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # 1. Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Connect and start a transaction
    connection = await engine.connect()
    transaction = await connection.begin()

    # 3. Create a session bound to this specific connection/transaction
    Session = sessionmaker(bind=connection, class_=AsyncSession, expire_on_commit=False)
    session = Session()

    yield session

    # 4. Cleanup: Rollback everything so no data persists
    await session.close()
    await transaction.rollback()
    await connection.close()
    await engine.dispose()
