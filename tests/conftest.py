"""Pytest configuration and shared fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from main import app

# Create test database
TEST_DATABASE_URL = "sqlite:///./test_cache.db"
test_engine = create_engine(TEST_DATABASE_URL, echo=False)

@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test"""
    # Create tables
    SQLModel.metadata.create_all(test_engine)
    
    # Override the engine in main module
    import main
    main.engine = test_engine
    
    yield test_engine
    
    # Clean up
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture
def client(test_db):
    """Create test client"""
    return TestClient(app)
