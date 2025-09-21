"""Integration tests"""
import pytest
from sqlmodel import Session, select
from main import CacheEntry

class TestIntegration:
    """Integration tests"""
    
    def test_full_workflow(self, client, test_db):
        """Test complete workflow: create payload, retrieve it, verify caching"""
        # Create payload
        payload_data = {
            "list_1": ["test", "string"],
            "list_2": ["another", "word"]
        }
        
        create_response = client.post("/payload", json=payload_data)
        assert create_response.status_code == 200
        payload_id = create_response.json()["id"]
        
        # Retrieve payload
        get_response = client.get(f"/payload/{payload_id}")
        assert get_response.status_code == 200
        assert get_response.json()["output"] == "TEST, ANOTHER, STRING, WORD"
        
        # Create another payload with same strings (should use cache)
        payload_data2 = {
            "list_1": ["test", "string"],
            "list_2": ["different", "words"]
        }
        
        create_response2 = client.post("/payload", json=payload_data2)
        assert create_response2.status_code == 200
        
        # Verify cache was used (check database)
        with Session(test_db) as session:
            cached_entries = session.exec(select(CacheEntry)).all()
            assert len(cached_entries) == 6  # test, string, another, word, different, words
            assert any(entry.input_text == "test" for entry in cached_entries)
            assert any(entry.input_text == "string" for entry in cached_entries)
            assert any(entry.input_text == "another" for entry in cached_entries)
            assert any(entry.input_text == "word" for entry in cached_entries)
            assert any(entry.input_text == "different" for entry in cached_entries)
            assert any(entry.input_text == "words" for entry in cached_entries)
    
    def test_cache_reuse_across_payloads(self, client, test_db):
        """Test that cache is reused across different payloads"""
        # Create first payload
        payload_data1 = {
            "list_1": ["hello", "world"],
            "list_2": ["foo", "bar"]
        }
        
        response1 = client.post("/payload", json=payload_data1)
        assert response1.status_code == 200
        
        # Create second payload with overlapping strings
        payload_data2 = {
            "list_1": ["hello", "new"],
            "list_2": ["bar", "test"]
        }
        
        response2 = client.post("/payload", json=payload_data2)
        assert response2.status_code == 200
        
        # Verify cache entries
        with Session(test_db) as session:
            cached_entries = session.exec(select(CacheEntry)).all()
            # Should have: hello, world, foo, bar, new, test = 6 entries
            assert len(cached_entries) == 6
            
            # Verify specific strings are cached
            input_texts = [entry.input_text for entry in cached_entries]
            assert "hello" in input_texts
            assert "world" in input_texts
            assert "foo" in input_texts
            assert "bar" in input_texts
            assert "new" in input_texts
            assert "test" in input_texts
    
    def test_multiple_identical_payloads(self, client, test_db):
        """Test creating multiple identical payloads"""
        payload_data = {
            "list_1": ["same", "data"],
            "list_2": ["test", "case"]
        }
        
        # Create first payload
        response1 = client.post("/payload", json=payload_data)
        assert response1.status_code == 200
        payload_id1 = response1.json()["id"]
        
        # Create second identical payload
        response2 = client.post("/payload", json=payload_data)
        assert response2.status_code == 200
        payload_id2 = response2.json()["id"]
        
        # Payloads should have different IDs
        assert payload_id1 != payload_id2
        
        # But both should have same output
        get_response1 = client.get(f"/payload/{payload_id1}")
        get_response2 = client.get(f"/payload/{payload_id2}")
        
        assert get_response1.json()["output"] == get_response2.json()["output"]
        assert get_response1.json()["output"] == "SAME, TEST, DATA, CASE"
        
        # Cache should only have 4 entries (same, data, test, case)
        with Session(test_db) as session:
            cached_entries = session.exec(select(CacheEntry)).all()
            assert len(cached_entries) == 4
