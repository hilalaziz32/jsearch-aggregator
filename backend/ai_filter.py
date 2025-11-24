"""
AI-Powered Job Filtering Module

This module scrapes job links, uses Gemini AI to analyze companies,
and filters jobs based on company size (keeping SMBs, filtering out big companies).
"""

import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from difflib import SequenceMatcher
import os
from typing import Dict, List, Optional
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Fuzzy matching threshold (70% match with "yes")
FUZZY_THRESHOLD = 0.7


def scrape_job_link(url: str, timeout: int = 10) -> Optional[str]:
    """
    Scrapes the job posting link and extracts relevant text content.
    
    Args:
        url: The job posting URL to scrape
        timeout: Request timeout in seconds
        
    Returns:
        Scraped text content or None if scraping fails
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Limit text length to avoid token limits (first 3000 characters)
        return text[:3000] if text else None
        
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {str(e)}")
        return None


def analyze_with_gemini(job_data: Dict, scraped_content: Optional[str] = None) -> str:
    """
    Uses Gemini AI to analyze if a job is from a big company or SMB.
    
    Args:
        job_data: Job data from RapidAPI
        scraped_content: Scraped content from job link (optional)
        
    Returns:
        AI response (should be "yes" or "no")
    """
    
    if not GEMINI_API_KEY:
        print("⚠️ Warning: GEMINI_API_KEY not set. Defaulting to 'yes' for all jobs.")
        return "yes"
    
    try:
        # Prepare job information for AI analysis
        job_info = f"""
Job Title: {job_data.get('job_title', 'N/A')}
Employer Name: {job_data.get('employer_name', 'N/A')}
Company Type: {job_data.get('employer_company_type', 'N/A')}
Employer Website: {job_data.get('employer_website', 'N/A')}
Location: {job_data.get('job_location', 'N/A')}
Job Description: {job_data.get('job_description', 'N/A')[:500]}
NAICS Code: {job_data.get('job_naics_code', 'N/A')}
NAICS Name: {job_data.get('job_naics_name', 'N/A')}
"""
        
        if scraped_content:
            job_info += f"\n\nScraped Content from Job Link:\n{scraped_content[:1000]}"
        
        # Create prompt for Gemini
        prompt = f"""You are an expert at analyzing companies and identifying their size.

Analyze the following job posting details and determine if this job is from a SMALL or MEDIUM business ONLY.

{job_info}

CRITICAL RULES:
- ONLY accept: Small businesses (under 100 employees) or Medium businesses (100-500 employees)
- REJECT everything else:
  * Large companies (500+ employees)
  * Enterprise companies
  * Fortune 500/1000 companies
  * Well-known corporations (Google, Amazon, Microsoft, Apple, Meta, etc.)
  * Advanced medium or large-medium businesses
  * Any company with thousands of employees
  * Public companies with large market cap
  * Big tech companies
  * Large consulting firms

If it's a SMALL or MEDIUM business (SMB) ONLY, answer: yes
If it's anything larger than medium business, answer: no

Answer with ONLY ONE WORD: "yes" or "no"
"""
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Extract text response
        ai_response = response.text.strip().lower()
        
        print(f"🤖 AI Response for {job_data.get('employer_name', 'Unknown')}: {ai_response}")
        
        return ai_response
        
    except Exception as e:
        print(f"❌ Error calling Gemini AI: {str(e)}")
        # Default to "yes" if AI fails
        return "yes"


def fuzzy_match_yes(ai_response: str, threshold: float = FUZZY_THRESHOLD) -> bool:
    """
    Uses fuzzy matching to determine if AI response matches "yes".
    
    Args:
        ai_response: The response from AI
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        True if response fuzzy matches "yes", False otherwise
    """
    
    # Clean the response
    cleaned_response = ai_response.strip().lower()
    
    # Calculate similarity ratio with "yes"
    similarity = SequenceMatcher(None, cleaned_response, "yes").ratio()
    
    print(f"🎯 Fuzzy match: '{cleaned_response}' vs 'yes' = {similarity:.2%} (threshold: {threshold:.0%})")
    
    return similarity >= threshold


def filter_job_with_ai(job_data: Dict, scrape_links: bool = True) -> bool:
    """
    Main filtering function that decides if a job should be kept.
    
    Args:
        job_data: Job data object from RapidAPI
        scrape_links: Whether to scrape job links for additional context
        
    Returns:
        True if job should be kept, False if it should be removed
    """
    
    print(f"\n🔍 Analyzing job: {job_data.get('job_title', 'Unknown')} @ {job_data.get('employer_name', 'Unknown')}")
    
    # Step 1: Get job apply link
    scraped_content = None
    if scrape_links:
        job_link = job_data.get('job_apply_link')
        if job_link:
            print(f"🌐 Scraping job link: {job_link[:60]}...")
            scraped_content = scrape_job_link(job_link)
            if scraped_content:
                print(f"✅ Scraped {len(scraped_content)} characters")
            else:
                print("⚠️ Scraping failed or returned no content")
    
    # Step 2: Analyze with Gemini AI
    ai_response = analyze_with_gemini(job_data, scraped_content)
    
    # Step 3: Fuzzy match AI response with "yes"
    should_keep = fuzzy_match_yes(ai_response)
    
    # Step 4: Return decision
    decision = "✅ KEEP" if should_keep else "❌ REMOVE"
    print(f"{decision} - {job_data.get('employer_name', 'Unknown')}\n")
    
    return should_keep


def filter_jobs_batch(job_list: List[Dict], scrape_links: bool = True, delay: float = 0.5) -> List[Dict]:
    """
    Filters a batch of jobs using AI analysis.
    
    Args:
        job_list: List of job objects from RapidAPI
        scrape_links: Whether to scrape job links
        delay: Delay between API calls (to avoid rate limiting)
        
    Returns:
        Filtered list of jobs (only kept jobs)
    """
    
    print(f"\n{'='*60}")
    print(f"🚀 Starting AI-powered job filtering")
    print(f"📊 Total jobs to analyze: {len(job_list)}")
    print(f"{'='*60}\n")
    
    filtered_jobs = []
    
    for idx, job in enumerate(job_list, 1):
        print(f"[{idx}/{len(job_list)}]", end=" ")
        
        # Filter job
        should_keep = filter_job_with_ai(job, scrape_links=scrape_links)
        
        if should_keep:
            filtered_jobs.append(job)
        
        # Add delay to avoid rate limiting
        if idx < len(job_list):
            time.sleep(delay)
    
    print(f"\n{'='*60}")
    print(f"✅ Filtering complete!")
    print(f"📊 Original jobs: {len(job_list)}")
    print(f"✅ Kept jobs: {len(filtered_jobs)}")
    print(f"❌ Removed jobs: {len(job_list) - len(filtered_jobs)}")
    print(f"{'='*60}\n")
    
    return filtered_jobs

