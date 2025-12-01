"""
AI-Powered Job Filtering Module (Simplified)

This module analyzes job data from RapidAPI using Gemini AI
to identify and filter jobs based on company size (keeping SMBs).
No web scraping - direct analysis of API-returned data.
"""

import google.generativeai as genai
import os
import logging
from typing import Dict, List
from dotenv import load_dotenv

# Setup logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("✅ Gemini AI configured successfully")
    except Exception as e:
        logger.error(f"❌ Failed to configure Gemini: {str(e)}")
        GEMINI_API_KEY = None

# Big company keywords to filter out
BIG_COMPANY_KEYWORDS = [
    'amazon', 'google', 'microsoft', 'apple', 'meta', 'facebook',
    'netflix', 'adobe', 'oracle', 'salesforce', 'ibm', 'intel',
    'cisco', 'nvidia', 'qualcomm', 'broadcom', 'amd', 'vmware',
    'workday', 'servicenow', 'slack', 'zoom', 'stripe', 'square',
    'uber', 'airbnb', 'lyft', 'doordash', 'instacart', 'spotify',
    'twitch', 'github', 'gitlab', 'dropbox', 'box', 'asana',
    'monday', 'notion', 'figma', 'sketch', 'invision', 'framer',
    'webflow', 'wix', 'squarespace', 'shopify', 'magento', 'bigcommerce',
    'walmart', 'target', 'costco', 'kroger', 'safeway', 'home depot',
    'lowes', 'best buy', 'dell', 'hp', 'lenovo', 'canon', 'sony',
    'samsung', 'lg', 'panasonic', 'toyota', 'honda', 'ford', 'gm',
    'tesla', 'byd', 'vw', 'bmw', 'mercedes', 'audi', 'porsche',
    'jpmorgan', 'goldman', 'morgan stanley', 'bank of america',
    'wells fargo', 'citigroup', 'ubs', 'barclays', 'hsbc', 'bnp paribas',
    'deutsche bank', 'credit suisse', 'nomura', 'mizuho', 'sumitomo',
    'mitsubishi ufj', 'softbank', 'rakuten', 'gree', 'dena',
    'accenture', 'deloitte', 'pwc', 'ey', 'kpmg', 'mckinsey',
    'bcg', 'bain', 'cap gemini', 'cognizant', 'wipro', 'tcs',
    'infosys', 'hcl', 'tech mahindra', 'mindtree', 'ltts', 'persistent',
    'us army', 'us navy', 'us air force', 'us marine', 'doe', 'dod',
    'nasa', 'nsa', 'dia', 'state department', 'defense contractor'
]


def is_big_company(company_name: str, job_data: Dict) -> bool:
    """
    Checks if a company is a big company using simple keyword matching.
    
    Args:
        company_name: Company name to check
        job_data: Full job data dictionary
        
    Returns:
        True if company appears to be a big company, False otherwise
    """
    company_lower = company_name.lower()
    
    # Check against keyword list
    for keyword in BIG_COMPANY_KEYWORDS:
        if keyword in company_lower:
            logger.debug(f"🏢 Big company detected: {company_name} (matched: {keyword})")
            return True
    
    # Check company type if available
    company_type = job_data.get('employer_company_type', '').lower()
    if 'corporation' in company_type or 'public' in company_type or 'enterprise' in company_type:
        # Could be big, but not definitive
        logger.debug(f"📊 Potential large company type: {company_type}")
    
    return False


def analyze_with_gemini(job_data: Dict) -> bool:
    """
    Uses Gemini AI to analyze if a job should be kept (SMB) or filtered (big company).
    
    Args:
        job_data: Job data from RapidAPI
        
    Returns:
        True if job should be kept (SMB), False if it should be filtered (big company)
    """
    
    if not GEMINI_API_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not configured. Using keyword matching only.")
        return True
    
    try:
        # Prepare job information for AI analysis
        job_info = f"""
Analyze this job posting to determine if it's from a Small-to-Medium Business (SMB) or a Big Company.

Job Title: {job_data.get('job_title', 'N/A')}
Employer Name: {job_data.get('employer_name', 'N/A')}
Company Type: {job_data.get('employer_company_type', 'N/A')}
Employer Website: {job_data.get('employer_website', 'N/A')}
Location: {job_data.get('job_location', 'N/A')}
Job Description (first 500 chars): {job_data.get('job_description', 'N/A')[:500]}

Based on the information above, is this job from a Small-to-Medium Business (SMB)?
Answer ONLY with 'yes' or 'no'.
yes = SMB (keep the job)
no = Big Company (filter it out)
"""
        
        # Call Gemini API
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(job_info, stream=False)
        
        if response and response.text:
            answer = response.text.strip().lower()
            is_smb = 'yes' in answer
            logger.debug(f"🤖 Gemini analysis for {job_data.get('employer_name')}: {answer} -> {'KEEP' if is_smb else 'FILTER'}")
            return is_smb
        else:
            logger.warning("⚠️ No response from Gemini")
            return True
            
    except Exception as e:
        logger.error(f"❌ Gemini analysis error: {str(e)}")
        logger.warning("⚠️ Falling back to keyword matching")
        return not is_big_company(job_data.get('employer_name', ''), job_data)


def filter_jobs_batch(jobs: List[Dict], scrape_links: bool = False, delay: float = 0.5) -> List[Dict]:
    """
    Filter jobs to keep only SMB positions, removing big company jobs.
    
    Args:
        jobs: List of job dictionaries from RapidAPI
        scrape_links: Ignored (kept for compatibility)
        delay: Ignored (kept for compatibility)
        
    Returns:
        Filtered list of jobs (only SMB jobs)
    """
    
    logger.info(f"🔍 Filtering {len(jobs)} jobs...")
    filtered_jobs = []
    
    for i, job in enumerate(jobs):
        company_name = job.get('employer_name', 'Unknown')
        
        try:
            # First check with fast keyword matching
            if is_big_company(company_name, job):
                logger.debug(f"⏭️ Skipping {company_name} (keyword match)")
                continue
            
            # Then check with AI analysis if available
            if GEMINI_API_KEY:
                if analyze_with_gemini(job):
                    filtered_jobs.append(job)
                    logger.debug(f"✅ Kept: {company_name}")
                else:
                    logger.debug(f"❌ Filtered: {company_name}")
            else:
                # No AI, keep jobs that pass keyword check
                filtered_jobs.append(job)
                logger.debug(f"✅ Kept: {company_name} (keyword match)")
                
        except Exception as e:
            logger.error(f"❌ Error processing {company_name}: {str(e)}")
            # Keep the job if there's an error
            filtered_jobs.append(job)
    
    logger.info(f"📊 Filtering complete: {len(jobs)} → {len(filtered_jobs)} jobs")
    return filtered_jobs
