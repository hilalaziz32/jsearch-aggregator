import requests
import json
import os
import re

# --- CONFIGURATION (EASY TO CHANGE) ---

# Your RapidAPI Key for the JSearch API (as provided in your request)
RAPIDAPI_KEY = '3733bc90bdmsh3a4e3a23d0b9629p179849jsnbf97a06e60ed'

# Search Parameters
SEARCH_QUERY = 'Patient Coordinator, Clinic Front Desk, Medical Office Assistant jobs in New York'
NUM_PAGES = 2
COUNTRY = 'us'

# API Endpoint
API_URL = 'https://jsearch.p.rapidapi.com/search'

# --- HTML TEMPLATE FUNCTIONS ---

def generate_job_accordion(job_data, index):
    """Generates the HTML for a single, collapsible job entry."""
    job_title = job_data.get('job_title', 'N/A')
    employer_name = job_data.get('employer_name', 'N/A')
    location = job_data.get('job_location', 'N/A')
    employment_type = job_data.get('job_employment_type', 'N/A')
    posted_at = job_data.get('job_posted_at', 'N/A')
    apply_link = job_data.get('job_apply_link')
    description = job_data.get('job_description', 'No detailed description available.').replace('\n', '<br>')
    
    # Format salary if available
    min_salary = job_data.get('job_min_salary')
    max_salary = job_data.get('job_max_salary')
    salary_period = job_data.get('job_salary_period')
    
    salary_str = "N/A"
    if min_salary and max_salary and salary_period:
        salary_str = f"${min_salary:,} - ${max_salary:,} ({salary_period})"
    elif job_data.get('job_salary'):
        salary_str = job_data['job_salary']

    # Use a descriptive link for the apply URL
    apply_link_html = f'<a href="{apply_link}" target="_blank">Apply Here</a>' if apply_link else 'N/A'
    
    # Accordion Structure
    return f"""
    <div class="job-card">
        <input type="checkbox" id="job{index}" class="accordion-toggle">
        <label for="job{index}" class="accordion-header">
            <span class="job-title-label">Job Title:</span>
            <span class="job-title-text">{job_title}</span>
            <span class="location-text"> @ {location}</span>
        </label>
        <div class="accordion-content">
            <p><strong>Employer:</strong> {employer_name}</p>
            <p><strong>Location:</strong> {location}</p>
            <p><strong>Type:</strong> {employment_type}</p>
            <p><strong>Posted:</strong> {posted_at}</p>
            <p><strong>Salary:</strong> {salary_str}</p>
            <p class="apply-link"><strong>Apply Link:</strong> {apply_link_html}</p>
            <div class="description-section">
                <h4>Job Description:</h4>
                <p>{description}</p>
            </div>
        </div>
    </div>
    """

def create_full_html(job_list, query, request_id):
    """Generates the full HTML file content."""
    
    total_jobs = len(job_list)
    job_accordions = "".join([generate_job_accordion(job, i) for i, job in enumerate(job_list)])
    
    # CSS for the 'nice easy to read well formatted' style and accordion
    css = """
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f9; color: #333; margin: 20px; }
    .container { max-width: 900px; margin: 0 auto; background-color: #ffffff; padding: 20px 40px; border-radius: 12px; box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1); }
    h1 { color: #007bff; text-align: center; border-bottom: 3px solid #007bff; padding-bottom: 10px; margin-bottom: 25px; }
    .summary { text-align: center; margin-bottom: 30px; font-size: 1.1em; color: #555; }
    .job-card { border: 1px solid #ddd; margin-bottom: 10px; border-radius: 8px; overflow: hidden; background-color: #fdfdff; }
    .accordion-toggle { display: none; }
    .accordion-header { display: block; padding: 15px; cursor: pointer; background-color: #e9ecef; color: #333; transition: background-color 0.3s; font-weight: bold; position: relative; }
    .accordion-header:hover { background-color: #d8dde3; }
    .accordion-header::after { content: '\\25B6'; /* Right triangle */ position: absolute; right: 15px; top: 50%; transform: translateY(-50%); transition: transform 0.3s; }
    .accordion-toggle:checked + .accordion-header::after { content: '\\25BC'; /* Down triangle */ }
    .accordion-toggle:checked + .accordion-header { background-color: #007bff; color: white; }
    .accordion-content { max-height: 0; overflow: hidden; transition: max-height 0.3s ease-out, padding 0.3s; padding: 0 15px; }
    .accordion-toggle:checked ~ .accordion-content { max-height: 1000px; /* Large enough value */ padding: 15px; border-top: 1px solid #ddd; }
    .job-title-label { color: #007bff; margin-right: 5px; }
    .job-title-text { color: #333; }
    .location-text { font-size: 0.9em; font-weight: normal; color: #6c757d; }
    .apply-link a { color: #28a745; text-decoration: none; font-weight: bold; }
    .apply-link a:hover { text-decoration: underline; }
    .description-section { margin-top: 15px; border-top: 1px dashed #ccc; padding-top: 10px; }
    .description-section h4 { color: #007bff; margin-top: 0; }
    """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job Search Results: {query}</title>
        <style>{css}</style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Job Search Results</h1>
            <div class="summary">
                <p><strong>Query:</strong> {query} | <strong>Total Jobs Found:</strong> {total_jobs} | <strong>Request ID:</strong> {request_id}</p>
            </div>
            {job_accordions}
        </div>
    </body>
    </html>
    """
    return html

# --- MAIN EXECUTION ---

def fetch_and_generate_html():
    """Fetches data from the API and generates the HTML file."""
    
    print(f"Starting job search for: '{SEARCH_QUERY}'")
    
    # 1. Setup API Request
    querystring = {
        "query": SEARCH_QUERY,
        "page": str(1),
        "num_pages": str(NUM_PAGES),
        "country": COUNTRY,
        "date_posted": "all"
    }
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    
    try:
        # 2. Make API Call
        response = requests.get(API_URL, headers=headers, params=querystring, timeout=15)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return

    # 3. Process Data
    job_data_list = data.get('data', [])
    request_id = data.get('request_id', 'unknown-id')
    
    if not job_data_list:
        print("API returned no job data. Exiting.")
        return

    # 4. Generate HTML
    html_content = create_full_html(job_data_list, SEARCH_QUERY, request_id)
    
    # 5. Save File
    # Use the first 8 digits of the request_id for the filename
    filename_prefix = request_id.split('-')[0][:8]
    filename = f"{filename_prefix}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"\n✅ Success! HTML file created: **{filename}**")
    print(f"Total Jobs Displayed: **{len(job_data_list)}**")
    print("Open the file in your web browser to view the results.")

if __name__ == "__main__":
    fetch_and_generate_html()
