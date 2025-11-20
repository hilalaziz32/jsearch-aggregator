# Job Search API Backend

FastAPI backend for searching jobs and generating formatted HTML/XLSX results.

## Features

- RESTful API for job searching
- HTML output with collapsible job listings
- XLSX export functionality
- Configurable CORS settings
- Environment-based configuration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the server:
```bash
python main.py
```

## Environment Configuration

Create a `.env` file with the following variables:

### Required
- `RAPIDAPI_KEY`: Your RapidAPI key for JSearch API

### Optional
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins (default: "*")
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)

### Example .env file:
```env
RAPIDAPI_KEY=your_rapidapi_key_here
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000
```

## API Endpoints

- `GET /` - API information
- `POST /search` - Search for jobs (returns HTML)
- `GET /export/xlsx/{request_id}` - Export results to XLSX
- `GET /docs` - Interactive API documentation

## Development

### Running with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API:
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "software engineer", "num_pages": 2}'
```

## Production Notes

- Set `CORS_ALLOWED_ORIGINS` to specific domains in production
- Consider using a proper API key management system
- The backend uses in-memory caching for job data (resets on server restart)
