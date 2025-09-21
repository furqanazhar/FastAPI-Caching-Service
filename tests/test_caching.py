"""Tests for caching functionality"""
import pytest
from sqlmodel import Session, select
from main import get_cached_result, CacheEntry

class TestCaching:
    """Test caching functionality"""
    
    def test_get_cached_result_miss(self, test_db):
        """Test cache miss - should transform and cache"""
        result = get_cached_result("hello")
        assert result == "HELLO"
        
        # Verify it was cached
        with Session(test_db) as session:
            cached = session.exec(select(CacheEntry).where(CacheEntry.input_text == "hello")).first()
            assert cached is not None
            assert cached.transformed_text == "HELLO"
    
    def test_get_cached_result_hit(self, test_db):
        """Test cache hit - should return cached result"""
        # First call - cache miss
        result1 = get_cached_result("world")
        assert result1 == "WORLD"
        
        # Second call - cache hit
        result2 = get_cached_result("world")
        assert result2 == "WORLD"
        assert result1 == result2
    
    def test_multiple_cache_entries(self, test_db):
        """Test multiple cache entries"""
        # Cache multiple strings
        get_cached_result("test1")
        get_cached_result("test2")
        get_cached_result("test3")
        
        # Verify all are cached
        with Session(test_db) as session:
            cached_entries = session.exec(select(CacheEntry)).all()
            assert len(cached_entries) == 3
            
            input_texts = [entry.input_text for entry in cached_entries]
            assert "test1" in input_texts
            assert "test2" in input_texts
            assert "test3" in input_texts
    
    def test_cache_persistence(self, test_db):
        """Test that cache persists across multiple calls"""
        # First call
        result1 = get_cached_result("persistent")
        assert result1 == "PERSISTENT"
        
        # Second call should hit cache
        result2 = get_cached_result("persistent")
        assert result2 == "PERSISTENT"
        
        # Verify only one cache entry exists
        with Session(test_db) as session:
            cached_entries = session.exec(select(CacheEntry).where(CacheEntry.input_text == "persistent")).all()
            assert len(cached_entries) == 1
