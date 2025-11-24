# Job Search Application

A complete job search application with a modern frontend interface and FastAPI backend.

## Project Structure

```
hiring_report/
├── backend/
│   ├── main.py              # FastAPI backend with CORS support
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment configuration template
│   └── README.md           # Backend documentation
├── frontend/
│   ├── index.html          # Main interface
│   ├── styles.css          # Modern styling
│   ├── script.js           # Frontend logic
│   └── README.md           # Frontend documentation
├── docs/
│   └── API_REFERENCE.md    # API documentation
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Container orchestration
├── nginx.conf             # Nginx reverse proxy configuration
├── .env.example           # Root environment configuration template
└── README.md              # This file
```

## Quick Start

### Docker Setup (Recommended)
1. Copy environment configuration:
   ```bash
   cp .env.example .env
   # Edit .env with your RapidAPI key
   ```

2. Build and start containers:
   ```bash
   docker-compose up --build
   ```

3. Open `http://localhost:5555` in your browser

### Manual Setup (Development)

#### Backend Setup
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your RapidAPI key
   ```

4. Start the backend:
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`

#### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Start a local server:
   ```bash
   python3 -m http.server 8080
   ```

3. Open `http://localhost:8080` in your browser

## Features

### AI-Powered Job Filtering 🤖

The system intelligently filters job postings to keep only opportunities from small-medium businesses and startups:

1. **Automatic Web Scraping**: When RapidAPI returns job links, the system automatically scrapes them for additional context
2. **AI Analysis**: Google Gemini 2.0 Flash analyzes each job posting including:
   - Company name, type, and website
   - Job description and requirements
   - Industry codes (NAICS)
   - Scraped content from job links
3. **STRICT SMB Filtering**: AI only keeps jobs from:
   - **Small businesses**: Under 100 employees
   - **Medium businesses**: 100-500 employees
   - **Rejects**: Large companies, enterprise, Fortune 500, big tech, advanced medium, anything 500+ employees
4. **Fuzzy Matching**: Uses difflib.SequenceMatcher with 70% threshold to handle AI response variations
5. **Object-by-Object Processing**: Each job is analyzed individually for accuracy

**Result**: Only jobs from true SMBs (small and medium businesses) are returned - everything else is filtered out!

### Frontend
- **Clean Interface**: Simple search bar with advanced options
- **Responsive Design**: Works on desktop and mobile
- **Advanced Settings**: Collapsible configuration panel with AI filter toggles
- **Real-time Results**: Direct HTML rendering from backend
- **Enhanced UX**: Only one job card expanded at a time
- **Export Functionality**: XLSX download links
- **Keyboard Shortcuts**: Quick search and clear functionality
- **AI Filter Controls**: Toggle AI filtering and link scraping on/off

### Backend
- **FastAPI**: Modern, fast Python web framework
- **🤖 AI-Powered Filtering**: Uses Google Gemini 2.0 Flash to filter out big company jobs
- **🌐 Automatic Web Scraping**: Scrapes job links for enhanced AI analysis
- **🎯 Intelligent Matching**: Fuzzy matching with difflib to interpret AI responses
- **CORS Support**: Configurable cross-origin requests
- **Environment Configuration**: Secure API key management
- **HTML Generation**: Beautiful, collapsible job listings
- **XLSX Export**: Professional spreadsheet downloads with all fields
- **Error Handling**: Comprehensive error responses

## API Endpoints

When running with Docker (recommended):
- `GET /` - Frontend interface
- `POST /api/search` - Search jobs (returns HTML)
- `GET /api/export/xlsx/{request_id}` - Export to Excel
- `GET /api/docs` - Interactive API documentation

When running manually:
- `GET /` - API information
- `POST /search` - Search jobs (returns HTML)
- `GET /export/xlsx/{request_id}` - Export to Excel
- `GET /docs` - Interactive API documentation

## Environment Configuration

The backend supports environment variables via `.env` file:

- `RAPIDAPI_KEY` (required): Your JSearch API key from [RapidAPI](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
- `GEMINI_API_KEY` (required): Your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- `CORS_ALLOWED_ORIGINS` (optional): Comma-separated allowed origins
- `HOST` (optional): Server host (default: 0.0.0.0)
- `PORT` (optional): Server port (default: 8000)

## Development

### Backend Development
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
The frontend is static HTML/CSS/JS - just open `frontend/index.html` in a browser or use a local server.

## Production Deployment

### Deploying to Render

You can deploy this project to [Render](https://render.com) using Docker:

1. **Add your secrets:**
   - Set your `RAPIDAPI_KEY` and `ADMIN_PASSWORD` in the Render dashboard as environment variables.
   - Optionally set `CORS_ALLOWED_ORIGINS` for security (e.g., your frontend URL).

2. **Create a new Web Service:**
   - Choose "Docker" as the environment.
   - Point to this repo and select the `Dockerfile`.
   - Set the Start Command to default (Render will use CMD from Dockerfile).
   - Set the port to `8000` (Render automatically sets the `PORT` env var).

3. **(Optional) Use render.yaml:**
   - You can commit the provided `render.yaml` to your repo for automatic configuration.

4. **Access your app:**
   - Once deployed, your backend will be available at `https://your-app-name.onrender.com`.
   - The frontend can be served from the same container (via nginx) or separately.

#### Required Environment Variables

- `RAPIDAPI_KEY`: Your JSearch API key (required)
- `ADMIN_PASSWORD`: Password for admin access (required)
- `CORS_ALLOWED_ORIGINS`: Comma-separated allowed origins (recommended)

#### Health Check

Set the health check path to `/` or `/docs` in the Render dashboard.

#### Scaling

For free tier, one instance is sufficient. For production, increase instance count as needed.


### Docker (Recommended)
- Use Docker Compose for easy deployment
- Set specific `CORS_ALLOWED_ORIGINS` in production
- Use proper secrets management for API keys
- Consider using a reverse proxy like Traefik or Nginx

### Manual Deployment

#### Backend
- Set specific `CORS_ALLOWED_ORIGINS` for security
- Use proper API key management
- Consider using a process manager like PM2 or systemd

#### Frontend
- Can be deployed to any static hosting service
- No build process required - pure HTML/CSS/JS
- Update API_BASE_URL in `script.js` if backend URL changes

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend is running and CORS is configured
2. **API Key Issues**: Verify RapidAPI key is set in `.env`
3. **Export Links**: Ensure backend can generate XLSX files
4. **Network Issues**: Check both frontend and backend are accessible

### Debugging
- Check browser console for JavaScript errors
- Verify backend logs for API request details
- Test API endpoints directly with curl or Postman

## License

This project is for demonstration purposes.
