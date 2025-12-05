# Job Search API

Production-ready FastAPI service for searching jobs via jsearch RapidAPI.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

Server runs on `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /health
```
## API Endpoints

### GET /health
Health check.

### POST /search
Search for jobs.

**Request:**
```json
{
  "api_key": "your_jsearch_key",
  "query": "Python Developer",
  "num_pages": 1,
  "country": "us",
  "date_posted": "all"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "your_key",
    "query": "Python Developer"
  }'
```

## Docs

Interactive API docs: `http://localhost:8000/docs`
