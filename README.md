# FastAPI Caching Service

A microservice built with FastAPI that provides caching functionality for string transformation operations. The service generates payloads by interleaving transformed strings from two input lists and caches the results to minimize external service calls.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **String Transformation Caching**: Caches transformer function results to minimize external service calls
- **Payload Generation**: Creates interleaved payloads from two string lists
- **Database Storage**: Uses SQLite/PostgreSQL for persistent caching
- **CLI Testing Tool**: Command-line interface for programmatic testing
- **Docker Support**: Containerized for easy deployment

## How It Works

The service implements a caching mechanism for string transformation operations:

1. **Input**: Two lists of strings (same length)
2. **Transformation**: Strings are processed by a transformer function (simulating external service)
3. **Interleaving**: Transformed strings are interleaved from both lists
4. **Caching**: Results are cached to minimize transformer function calls
5. **Storage**: Cached outcomes stored in SQLite/PostgreSQL database

## Quick Start

### Prerequisites

- Python 3.8+
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

## Project Structure

```
FastAPI-Caching-Service/
├── main.py              # Main FastAPI application
├── models.py            # SQLModel/SQLAlchemy models
├── cache_service.py     # Caching logic and transformer function
├── cli.py               # Command-line interface tool
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── tests/               # Unit and integration tests
│   ├── test_api.py
│   ├── test_cache.py
│   └── test_cli.py
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Docker Deployment

### Using Docker Compose

```bash
# Build and run the service
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

### Using Docker directly

```bash
# Build the image
docker build -t fastapi-caching-service .

# Run the container
docker run -p 8000:8000 fastapi-caching-service
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

### Environment Variables

Create a `.env` file in the root directory:

```env
# Application settings
APP_NAME=FastAPI Caching Service
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Database settings
DATABASE_URL=sqlite:///./cache.db
# For PostgreSQL: postgresql://user:password@localhost/dbname

# Cache settings
CACHE_TTL=300
CACHE_MAX_SIZE=1000
```

## Key Implementation Details

### Caching Strategy
- **Transformer Function**: Simulates external service calls for string transformation
- **Cache Reuse**: Minimizes calls to transformer function by caching results
- **Payload Deduplication**: Reuses payload identifiers for identical inputs
- **Database Persistence**: Stores cached outcomes in SQLite/PostgreSQL

### Technology Stack
- **FastAPI**: Web framework for building APIs
- **SQLModel/SQLAlchemy**: Database ORM for data persistence
- **Pydantic**: Data validation and settings management
- **Docker**: Containerization for deployment
- **pytest**: Testing framework

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes with meaningful messages (`git commit -m 'Add caching optimization'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Write clear and concise comments focusing on "why" not "how"
- Add unit and integration tests for new features
- Use meaningful commit messages in small, manageable chunks
