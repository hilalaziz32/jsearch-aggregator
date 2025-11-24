# Job Search API Reference

## Overview

The Job Search API provides a RESTful interface for searching job listings and returning formatted HTML results. It uses the JSearch API to fetch job data and generates beautifully formatted HTML with collapsible job listings.

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication is required for this API. The API key for the underlying JSearch service is configured server-side.

## Endpoints

### 1. Root Endpoint

**GET /** - Get API information

**Response:**
```json
{
  "message": "Job Search API",
  "version": "1.0.0",
  "endpoints": {
    "search": "/search (POST) - Search for jobs and get HTML results",
    "export": "/export/xlsx/{request_id} (GET) - Export job results to XLSX format",
    "docs": "/docs - Interactive API documentation"
  }
}
```

### 2. Search Jobs

**POST /search** - Search for jobs and return formatted HTML results with export capability

**Request Body:**
```json
{
  "query": "string (required)",
  "num_pages": "integer (optional, default: 2)",
  "country": "string (optional, default: 'us')",
  "date_posted": "string (optional, default: 'all')",
  "page": "integer (optional, default: 1)",
  "language": "string (optional)",
  "work_from_home": "boolean (optional, default: false)",
  "employment_types": "string (optional)",
  "job_requirements": "string (optional)",
  "radius": "integer (optional)",
  "exclude_job_publishers": "string (optional)",
  "fields": "string (optional)",
  "enable_ai_filter": "boolean (optional, default: true)",
  "scrape_links": "boolean (optional, default: true)"
}
```

**Parameters:**
- `query` (required): The search query string for job titles, keywords, or descriptions
- `num_pages` (optional): Number of pages to fetch from the job API (default: 2)
- `country` (optional): Country code for job search (default: "us")
- `date_posted` (optional): Date posted filter - "all", "today", "3days", "week", "month" (default: "all")
- `page` (optional): Starting page number for pagination (default: 1)
- `language` (optional): Language code for job postings (e.g., "en", "es", "fr")
- `work_from_home` (optional): Only return remote/work from home jobs (default: false)
- `employment_types` (optional): Comma-separated employment types - "FULLTIME", "CONTRACTOR", "PARTTIME", "INTERN"
- `job_requirements` (optional): Comma-separated job requirements - "under_3_years_experience", "more_than_3_years_experience", "no_experience", "no_degree"
- `radius` (optional): Search radius from location in kilometers
- `exclude_job_publishers` (optional): Comma-separated publishers to exclude (e.g., "BeeBe,Dice")
- `fields` (optional): Comma-separated fields to include in response (e.g., "employer_name,job_title,job_country")
- `enable_ai_filter` (optional): Use AI to filter out jobs from big companies (default: true)
- `scrape_links` (optional): Scrape job posting links for enhanced AI analysis (default: true)

**Response:**
- **Content-Type:** `text/html; charset=utf-8`
- **Status Codes:**
  - `200`: Success - Returns formatted HTML with job listings
  - `404`: No jobs found for the given criteria
  - `500`: Internal server error (API connection issues)

**Example Request:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "software engineer",
    "num_pages": 3,
    "country": "us",
    "date_posted": "week"
  }'
```

**Example Response (HTML):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Search Results: software engineer</title>
    <style>/* CSS styles for formatting */</style>
</head>
<body>
    <div class="container">
        <h1>🔍 Job Search Results</h1>
        <div class="summary">
            <p><strong>Query:</strong> software engineer | <strong>Total Jobs Found:</strong> 25 | <strong>Request ID:</strong> abc12345</p>
        </div>
        <div class="export-section">
            <a href="/export/xlsx/abc12345" class="export-button" download="software_e-16-11-2025.xlsx">
                📊 Export to Excel
            </a>
        </div>
        <!-- Collapsible job listings -->
    </div>
</body>
</html>
```

### 3. Export Jobs to XLSX

**GET /export/xlsx/{request_id}** - Export job search results to XLSX format

**Parameters:**
- `request_id` (required): The request ID returned from the job search endpoint

**Response:**
- **Content-Type:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- **Content-Disposition:** `attachment; filename="query-date.xlsx"`
- **Status Codes:**
  - `200`: Success - Returns XLSX file download
  - `404`: Job data not found for the given request ID
  - `500`: Internal server error generating XLSX file

**Example Request:**
```bash
curl -X GET "http://localhost:8000/export/xlsx/abc12345" \
  -H "Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  --output "software_e-16-11-2025.xlsx"
```

**XLSX File Features:**
- **Title Row**: Bold, centered column headers
- **Comprehensive Data**: Job title, employer, location, employment type, posted date, salary information, apply links, and descriptions
- **Auto-adjusted Columns**: Column widths automatically adjusted for readability
- **Professional Formatting**: Clean, professional spreadsheet layout
- **File Naming**: Files named using first 12 characters of search query and current date (e.g., "software_e-16-11-2025.xlsx")

## AI-Powered Filtering

When `enable_ai_filter` is set to `true` (default), the system:

1. **Scrapes Job Links**: Automatically scrapes job posting URLs to gather additional context
2. **AI Analysis**: Uses Google Gemini 2.0 Flash to analyze each job posting
3. **Company Size Detection**: AI determines if the company is:
   - Small Business (under 100 employees) → **KEEP**
   - Medium Business (100-500 employees) → **KEEP**
   - Large companies, enterprise, Fortune 500, or anything bigger → **REMOVE**
   - **STRICT FILTERING**: Only true SMBs are kept
4. **Fuzzy Matching**: Uses difflib.SequenceMatcher to interpret AI responses with 70% threshold
5. **Intelligent Filtering**: Only returns jobs from SMBs and smaller companies

**Environment Variable Required:**
- `GEMINI_API_KEY`: Your Google Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

## HTML Output Features

The returned HTML includes:

- **Responsive Design**: Works on desktop and mobile devices
- **Collapsible Job Cards**: Click to expand/collapse job details
- **Professional Styling**: Clean, modern design with proper spacing
- **Job Information**: Title, employer, location, type, salary, description
- **Apply Links**: Direct links to job application pages
- **Search Summary**: Query, total jobs found, and request ID
- **AI-Filtered Results**: Only jobs from SMBs and smaller companies (when enabled)

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK**: Successful request with HTML results
- **404 Not Found**: No jobs found for the search criteria
- **500 Internal Server Error**: Issues connecting to the JSearch API

Error responses include JSON with error details:
```json
{
  "detail": "Error message description"
}
```

## Usage Examples

### Python Example
```python
import requests

url = "http://localhost:8000/search"
data = {
    "query": "data scientist",
    "num_pages": 2,
    "country": "us"
}

response = requests.post(url, json=data)
if response.status_code == 200:
    html_content = response.text
    # Save to file or display
    with open("job_results.html", "w") as f:
        f.write(html_content)
else:
    print(f"Error: {response.json()}")
```

### JavaScript Example
```javascript
fetch('http://localhost:8000/search', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        query: 'frontend developer',
        num_pages: 2,
        country: 'us'
    })
})
.then(response => response.text())
.then(html => {
    document.body.innerHTML = html;
})
.catch(error => console.error('Error:', error));
```

## Running the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python main.py
```

3. Access the API at: `http://localhost:8000`

4. Interactive documentation available at: `http://localhost:8000/docs`

## Rate Limits

The API is subject to the rate limits of the underlying JSearch API service. No additional rate limiting is implemented in this wrapper.

## Notes

- The API key for JSearch is configured server-side and cannot be modified via API requests
- All job data is sourced from the JSearch API
- HTML output is optimized for readability and includes responsive design
- The API returns HTML content directly, not file downloads
