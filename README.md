# FastAPI Caching Service

A microservice built with FastAPI that provides caching functionality for string transformation operations. The service generates payloads by interleaving transformed strings from two input lists and caches the results to minimize external service calls.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **String Transformation Caching**: Caches transformer function results to minimize external service calls
- **Payload Generation**: Creates interleaved payloads from two string lists
- **Database Storage**: Uses local SQLite for persistent caching
- **CLI Testing Tool**: Command-line interface for programmatic testing
- **Docker Support**: Containerized for easy deployment

## How It Works

The service implements a caching mechanism for string transformation operations:

1. **Input**: Two lists of strings (same length)
2. **Transformation**: Strings are processed by a transformer function (simulating external service)
3. **Interleaving**: Transformed strings are interleaved from both lists
4. **Caching**: Results are cached to minimize transformer function calls
5. **Storage**: Cached outcomes stored in local SQLite database

## Quick Start

### Prerequisites

- Python 3.11
- pip (Python package installer)
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FastAPI-Caching-Service
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Create Payload
**POST** `/payload`

Creates a new payload by interleaving transformed strings from two input lists.

**Request Body:**
```json
{
  "list_1": ["first string", "second string", "third string"],
  "list_2": ["other string", "another string", "last string"]
}
```

**Response:**
```json
{
  "id": "uuid-identifier",
  "message": "Payload created successfully"
}
```

### Get Payload
**GET** `/payload/{id}`

Retrieves a previously created payload by its identifier.

**Response:**
```json
{
  "output": "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING, THIRD STRING, LAST STRING"
}
```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## CLI Testing Tool

The service includes a command-line interface for programmatic testing:

```bash
cache-cli [-h|--host URL] [-r|--repeat N] [-i|--input FILE|-] [-j|--json JSON] [-o|--output FILE|-] [-h|--help]
```

**Parameters:**
- `--host`: Points to the server URL (default: http://localhost:8000)
- `--repeat`: Number of iterations to run
- `--input`: Input file path ("-" for stdin)
- `--json`: Input argument in JSON format (properly escaped)
- `--output`: Output file path ("-" for stdout)
- `--help`: Show help message

**Examples:**
```bash
# Test with JSON input
cache-cli --json '{"list_1": ["hello", "world"], "list_2": ["foo", "bar"]}'

# Test with input file
cache-cli --input test_data.json --output results.json

# Test with repeat iterations
cache-cli --json '{"list_1": ["test"], "list_2": ["data"]}' --repeat 5
```

### Sample Input JSON Files

**Basic Example:**
```json
{
  "list_1": ["hello", "world", "test"],
  "list_2": ["foo", "bar", "data"]
}
```

**Single String Example:**
```json
{
  "list_1": ["single"],
  "list_2": ["string"]
}
```

**Longer Example:**
```json
{
  "list_1": ["first", "second", "third", "fourth", "fifth"],
  "list_2": ["alpha", "beta", "gamma", "delta", "epsilon"]
}
```

**Special Characters Example:**
```json
{
  "list_1": ["hello world!", "test@123", "camelCase"],
  "list_2": ["special chars", "numbers 456", "mixed_Case"]
}
```

**Expected Output:**
- Input: `["hello", "world"]` + `["foo", "bar"]`
- Output: `"HELLO, FOO, WORLD, BAR"`

## Project Structure

```
FastAPI-Caching-Service/
├── main.py              # Main FastAPI application with SQLModel
├── cli.py               # Command-line interface tool
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── test_data.json       # Sample test data for CLI
├── cache.db             # SQLite database (created at runtime)
├── tests/               # Test suite
│   ├── __init__.py      # Package marker
│   ├── conftest.py      # Shared fixtures and configuration
│   ├── test_transformer.py  # Transformer function tests
│   ├── test_caching.py      # Caching logic tests
│   ├── test_api.py          # API endpoint tests
│   └── test_integration.py  # Integration tests
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Docker Deployment


```bash
# Build the image
docker build -t fastapi-caching-service .

# Run without persistent data (data lost on restart)
docker run -p 8000:8000 fastapi-caching-service

# Run with persistent data (data survives restarts)
docker run -p 8000:8000 -v $(pwd):/app fastapi-caching-service
```

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_api.py
```

## Key Implementation Details

### Caching Strategy
- **Transformer Function**: Simulates external service calls for string transformation
- **Cache Reuse**: Minimizes calls to transformer function by caching results
- **Payload Deduplication**: Reuses payload identifiers for identical inputs
- **Database Persistence**: Stores cached outcomes in local SQLite

### Technology Stack
- **FastAPI**: Web framework for building APIs
- **SQLModel/SQLAlchemy**: Database ORM for data persistence
- **Pydantic**: Data validation and settings management
- **Docker**: Containerization for deployment
- **pytest**: Testing framework
