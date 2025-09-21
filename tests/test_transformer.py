"""Tests for transformer function"""
import pytest
from main import transformer_function

class TestTransformerFunction:
    """Test the transformer function"""
    
    def test_transformer_function(self):
        """Test string transformation"""
        assert transformer_function("hello") == "HELLO"
        assert transformer_function("world") == "WORLD"
        assert transformer_function("test") == "TEST"
        assert transformer_function("") == ""
    
    def test_transformer_function_special_characters(self):
        """Test transformation with special characters"""
        assert transformer_function("hello world!") == "HELLO WORLD!"
        assert transformer_function("test@123") == "TEST@123"
        assert transformer_function("camelCase") == "CAMELCASE"
    
    def test_transformer_function_numbers(self):
        """Test transformation with numbers"""
        assert transformer_function("test123") == "TEST123"
        assert transformer_function("123") == "123"
        assert transformer_function("test 123") == "TEST 123"
