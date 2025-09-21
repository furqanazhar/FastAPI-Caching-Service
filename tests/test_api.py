"""Tests for API endpoints"""

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "FastAPI Caching Service is running"}
    
    def test_create_payload_success(self, client, test_db):
        """Test successful payload creation"""
        payload_data = {
            "list_1": ["hello", "world"],
            "list_2": ["foo", "bar"]
        }
        
        response = client.post("/payload", json=payload_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert len(data["id"]) > 0  # Should have a UUID
    
    def test_create_payload_different_lengths(self, client):
        """Test payload creation with different list lengths"""
        payload_data = {
            "list_1": ["hello", "world"],
            "list_2": ["foo"]  # Different length
        }
        
        response = client.post("/payload", json=payload_data)
        assert response.status_code == 400
        assert "same length" in response.json()["detail"]
    
    def test_create_payload_empty_lists(self, client):
        """Test payload creation with empty lists"""
        payload_data = {
            "list_1": [],
            "list_2": []
        }
        
        response = client.post("/payload", json=payload_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
    
    def test_get_payload_success(self, client, test_db):
        """Test successful payload retrieval"""
        # First create a payload
        payload_data = {
            "list_1": ["hello", "world"],
            "list_2": ["foo", "bar"]
        }
        
        create_response = client.post("/payload", json=payload_data)
        assert create_response.status_code == 200
        
        payload_id = create_response.json()["id"]
        
        # Then retrieve it
        get_response = client.get(f"/payload/{payload_id}")
        assert get_response.status_code == 200
        
        data = get_response.json()
        assert "output" in data
        assert data["output"] == "HELLO, FOO, WORLD, BAR"
    
    def test_get_payload_not_found(self, client):
        """Test payload retrieval with non-existent ID"""
        response = client.get("/payload/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_get_payload_invalid_uuid(self, client):
        """Test payload retrieval with invalid UUID format"""
        response = client.get("/payload/invalid-uuid")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
