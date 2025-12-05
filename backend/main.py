from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- API Models ---

class JobSearchRequest(BaseModel):
    """Request model for job search"""
    api_key: str  # jsearch API key
    query: str
    num_pages: Optional[int] = 1
    page: Optional[int] = 1
    country: Optional[str] = "us"
    date_posted: Optional[str] = "all"
    remote_jobs_only: Optional[bool] = False
    employment_types: Optional[str] = None
    job_requirements: Optional[str] = None
    radius: Optional[int] = None

# --- API Configuration ---

app = FastAPI(
    title="Job Search API",
    description="Simple HTTP API to search jobs via jsearch",
    version="1.0.0"
)

# jsearch API configuration
JSEARCH_API_URL = "https://jsearch.p.rapidapi.com/search"

# CORS Configuration - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Endpoints ---

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "Job Search API"}

@app.post("/search")
async def search_jobs(request: JobSearchRequest):
    """
    Search for jobs using jsearch API and return raw JSON results
    
    Parameters:
    - api_key: Your jsearch RapidAPI key (required)
    - query: Job search query, e.g., "Python Developer" (required)
    - num_pages: Number of pages to fetch (default: 1)
    - page: Starting page number (default: 1)
    - country: Country code, e.g., "us", "uk", "ca" (default: "us")
    - date_posted: Date filter - "all", "today", "last_7_days", "last_30_days", "last_90_days" (default: "all")
    - remote_jobs_only: Only return remote jobs (default: false)
    - employment_types: Filter by type - "FULLTIME", "PARTTIME", "CONTRACT", "TEMPORARY" (optional)
    - job_requirements: Filter requirements - "under_3_years_experience", "3_plus_years_experience", etc (optional)
    - radius: Search radius in miles (optional)
    
    Returns: JSON object from jsearch API with job listings and metadata
    """
    
    try:
        # Build headers with the provided API key
        headers = {
            "x-rapidapi-key": request.api_key,
            "x-rapidapi-host": "jsearch.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        
        # Build query parameters
        params = {
            "query": request.query,
            "page": request.page,
            "num_pages": request.num_pages,
            "country": request.country,
            "date_posted": request.date_posted,
        }
        
        # Add optional parameters if provided
        if request.remote_jobs_only:
            params["remote_jobs_only"] = request.remote_jobs_only
        if request.employment_types:
            params["employment_types"] = request.employment_types
        if request.job_requirements:
            params["job_requirements"] = request.job_requirements
        if request.radius:
            params["radius"] = request.radius
        
        # Make request to jsearch API
        response = requests.get(JSEARCH_API_URL, headers=headers, params=params, timeout=30)
        
        # Check for errors
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"jsearch API error: {response.text}"
            )
        
        # Return the JSON response from jsearch
        return response.json()
    
    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Request to jsearch API timed out"
        )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calling jsearch API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
