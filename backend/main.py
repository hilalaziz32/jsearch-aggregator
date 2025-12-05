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

# --- FastAPI App Setup ---

app = FastAPI(
    title="Job Search API",
    description="Simple HTTP API to search jobs via jsearch",
    version="1.0.0"
)

# jsearch API configuration
JSEARCH_API_URL = "https://jsearch.p.rapidapi.com/search"

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Job Search API"}


@app.post("/search")
async def search_jobs(request: JobSearchRequest):

    try:
        # --- Headers (IMPORTANT: do NOT send Content-Type for GET) ---
        headers = {
            "x-rapidapi-key": request.api_key,
            "x-rapidapi-host": "jsearch.p.rapidapi.com"
        }

        # --- Build query params ---
        params = {
            "query": request.query,
            "page": request.page,
            "num_pages": request.num_pages,
            "country": request.country,
            "date_posted": request.date_posted,
        }

        if request.remote_jobs_only:
            params["remote_jobs_only"] = request.remote_jobs_only
        if request.employment_types:
            params["employment_types"] = request.employment_types
        if request.job_requirements:
            params["job_requirements"] = request.job_requirements
        if request.radius:
            params["radius"] = request.radius

        # --- Make request to jsearch ---
        response = requests.get(
            JSEARCH_API_URL,
            headers=headers,
            params=params,
            timeout=30
        )

        # Log important info to Render logs for debugging
        print("\n-----------------------------")
        print("JSEARCH STATUS:", response.status_code)
        print("JSEARCH TEXT:", response.text)
        print("-----------------------------\n")

        # If jsearch returns error
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"jsearch API error: {response.text}"
            )

        # Return the upstream JSON
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
        # Print full traceback for debugging
        import traceback
        print("ERROR TRACEBACK:\n", traceback.format_exc())
        print("ERROR TYPE:", type(e))
        print("ERROR MESSAGE:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


# --- Uvicorn runner for local use ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
