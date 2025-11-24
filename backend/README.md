# Job Search API Backend

FastAPI backend for searching jobs and generating formatted HTML/XLSX results.

## Features

- RESTful API for job searching
- **🤖 AI-Powered Filtering**: Uses Google Gemini 2.0 Flash to filter out big company jobs
- **🌐 Automatic Web Scraping**: Scrapes job posting links for enhanced analysis
- **🎯 Fuzzy Matching**: Intelligent AI response interpretation using difflib
- HTML output with collapsible job listings
- XLSX export functionality with all job data fields
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
- `GEMINI_API_KEY`: Your Google Gemini API key (for AI filtering)

### Optional
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins (default: "*")
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)

### Example .env file:
```env
RAPIDAPI_KEY=your_rapidapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000
```

### Getting API Keys
- **RapidAPI Key**: Sign up at [RapidAPI](https://rapidapi.com/) and subscribe to [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
- **Gemini API Key**: Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)

## API Endpoints

- `GET /` - API information
- `POST /search` - Search for jobs (returns HTML with AI-filtered results)
- `GET /export/xlsx/{request_id}` - Export results to XLSX
- `GET /docs` - Interactive API documentation

## AI Filtering

The system includes intelligent AI-powered filtering that:

1. **Scrapes Job Links**: Automatically fetches content from job posting URLs
2. **AI Analysis**: Uses Google Gemini 2.0 Flash to analyze:
   - Company name and type
   - Job description details
   - Employer website information
   - NAICS codes and industry data
   - Scraped content from job links
3. **Company Size Detection**: AI determines if the company is:
   - Small Business (under 100 employees) → ✅ KEEP
   - Medium Business (100-500 employees) → ✅ KEEP
   - Large companies, enterprise, Fortune 500, big tech → ❌ REMOVE
   - **STRICT**: Only keeps true SMBs, filters out everything larger
4. **Fuzzy Matching**: Uses `difflib.SequenceMatcher` with 70% threshold to interpret AI responses
5. **Object-by-Object Processing**: Each job is analyzed individually

### Disabling AI Filtering

You can disable AI filtering by setting `enable_ai_filter: false` in your API request:

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "software engineer",
    "enable_ai_filter": false
  }'
```

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
