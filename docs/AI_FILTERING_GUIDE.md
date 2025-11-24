# AI Filtering Usage Guide

## Overview

The Job Finder system now includes intelligent AI-powered filtering that automatically identifies and removes job postings from large corporations, keeping only opportunities from small-medium businesses (SMBs) and startups.

## How It Works

### Step 1: Job Search
When you search for jobs, RapidAPI returns a list of job postings with various details including:
- Job title and description
- Company name and information
- Job posting links
- Industry codes
- And more...

### Step 2: Web Scraping
For each job posting, the system:
- Extracts the job application link (`job_apply_link`)
- Scrapes the actual job posting page
- Gathers additional context (company info, job details)
- Limits content to 3000 characters to manage API costs

### Step 3: AI Analysis
Google Gemini 2.0 Flash analyzes each job posting:

**Input to AI:**
- Job title
- Employer name
- Company type
- Employer website
- Job location
- Job description
- NAICS code/name
- Scraped content from job link

**AI Prompt:**
```
Analyze the following job posting and determine if this job is from a 
SMALL or MEDIUM business ONLY.

CRITICAL RULES:
- ONLY accept: Small businesses (under 100 employees) or 
  Medium businesses (100-500 employees)
- REJECT everything else:
  * Large companies (500+ employees)
  * Enterprise companies
  * Fortune 500/1000 companies
  * Well-known corporations
  * Advanced medium or large-medium businesses
  * Any company with thousands of employees
  * Public companies with large market cap
  * Big tech companies

If it's a SMALL or MEDIUM business (SMB) ONLY, answer: yes
If it's anything larger than medium business, answer: no

Answer with ONLY ONE WORD: "yes" or "no"
```

### Step 4: Fuzzy Matching
The system uses Python's `difflib.SequenceMatcher` to interpret AI responses:

```python
similarity = SequenceMatcher(None, ai_response, "yes").ratio()
keep_job = similarity >= 0.7  # 70% threshold
```

This handles variations like:
- "yes" → 100% match → KEEP ✅
- "Yes" → 100% match → KEEP ✅
- "yess" → 75% match → KEEP ✅
- "no" → 33% match → REMOVE ❌
- "nope" → 40% match → REMOVE ❌

### Step 5: Filtering
- Jobs with "yes" (or similar) responses are **KEPT** ✅
- Jobs with "no" (or similar) responses are **REMOVED** ❌
- Only the filtered list is returned to the user

## Configuration

### Enable/Disable AI Filtering

**In the Frontend:**
1. Click "⚙️ Advanced Settings"
2. Check/uncheck "🤖 Enable AI Filtering"
3. Check/uncheck "🌐 Scrape Job Links"

**Via API:**
```json
{
  "query": "software engineer",
  "enable_ai_filter": true,
  "scrape_links": true
}
```

### Environment Setup

**Required Environment Variables:**
```bash
RAPIDAPI_KEY=your_rapidapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get Your API Keys:**
- **RapidAPI**: [Sign up here](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
- **Gemini**: [Get key here](https://makersuite.google.com/app/apikey)

## Performance Considerations

### Processing Time
- **Without AI Filter**: ~2-5 seconds for 20 jobs
- **With AI Filter**: ~20-40 seconds for 20 jobs
  - Web scraping: ~1 second per job
  - AI analysis: ~0.5 seconds per job
  - Delay between calls: 0.5 seconds (rate limiting)

### Rate Limiting
The system includes a 0.5-second delay between job analyses to avoid:
- Gemini API rate limits
- Web scraping blocks
- Excessive costs

### Cost Estimation
**Gemini 2.0 Flash Pricing (as of Nov 2024):**
- Input: ~$0.075 per 1M characters
- Output: ~$0.30 per 1M characters

**Example Cost:**
- 20 jobs × 3500 characters average = 70,000 characters input
- 20 responses × 10 characters = 200 characters output
- **Total cost: ~$0.006 per search** (less than a penny!)

## Troubleshooting

### AI Filter Not Working

**Check 1: Gemini API Key**
```bash
# Verify your .env file has the key
cat backend/.env | grep GEMINI_API_KEY
```

**Check 2: Backend Logs**
Look for these messages:
```
🤖 AI filtering enabled - starting analysis...
🔍 Analyzing job: [Job Title] @ [Company]
🤖 AI Response for [Company]: yes/no
✅ KEEP - [Company]
```

**Check 3: Error Messages**
If you see: `⚠️ Warning: GEMINI_API_KEY not set. Defaulting to 'yes' for all jobs.`
- Your API key is missing or incorrect

### Scraping Failures

Some job links cannot be scraped due to:
- JavaScript-heavy pages
- Bot protection (Cloudflare, etc.)
- Authentication requirements
- Rate limiting

**Solution:** The AI will still analyze using RapidAPI data only.

### All Jobs Filtered Out

If the AI removes all jobs:
```json
{
  "detail": "No jobs passed AI filtering. All jobs were from big companies."
}
```

**Solutions:**
1. Disable AI filtering temporarily
2. Adjust your search query
3. Try a different location or job type

## Examples

### Example 1: Keep Small Business
```
Job: "Frontend Developer at StartupXYZ"
Company: "StartupXYZ" (50 employees)
AI Analysis: "This is a small business with under 100 employees"
AI Response: "yes"
Fuzzy Match: 100%
Result: ✅ KEEP
```

### Example 2: Keep Medium Business
```
Job: "Developer at TechBoutique"
Company: "TechBoutique" (250 employees)
AI Analysis: "Medium business with 250 employees"
AI Response: "yes"
Fuzzy Match: 100%
Result: ✅ KEEP
```

### Example 3: Remove Big Company
```
Job: "Software Engineer at Google"
Company: "Google" (182,000+ employees)
AI Analysis: "This is a large enterprise with thousands of employees"
AI Response: "no"
Fuzzy Match: 33%
Result: ❌ REMOVE
```

### Example 4: Remove Large-Medium Company
```
Job: "Engineer at GrowthCorp"
Company: "GrowthCorp" (1,500 employees)
AI Analysis: "This is a large company exceeding 500 employees"
AI Response: "no"
Fuzzy Match: 33%
Result: ❌ REMOVE
```

### Example 3: Fuzzy Match Handling
```
Job: "Developer at LocalTech Inc"
Company: "LocalTech Inc" (25 employees)
AI Analysis: "Small local business"
AI Response: "yep" (typo or variation)
Fuzzy Match: 60% (below threshold)
Result: ❌ REMOVE (unfortunately)
```

## Best Practices

1. **Enable Scraping**: Always enable link scraping for better AI analysis
2. **Monitor Logs**: Watch backend logs to see AI decisions
3. **Adjust Queries**: Use specific job titles for better results
4. **Balance Speed vs Quality**: Disable AI filtering for quick searches
5. **API Key Security**: Never commit API keys to version control

## Advanced Configuration

### Adjust Fuzzy Match Threshold

Edit `backend/ai_filter.py`:
```python
# Default is 0.7 (70%)
FUZZY_THRESHOLD = 0.7

# More strict (requires closer match to "yes")
FUZZY_THRESHOLD = 0.85

# More lenient (accepts more variations)
FUZZY_THRESHOLD = 0.6
```

### Adjust Rate Limiting Delay

Edit `backend/main.py`:
```python
job_data_list = filter_jobs_batch(
    job_data_list, 
    scrape_links=request.scrape_links,
    delay=0.5  # Change this value (seconds)
)
```

### Change AI Model

Edit `backend/ai_filter.py`:
```python
# Current model
model = genai.GenerativeModel('gemini-2.5-flash')

# Alternative models
model = genai.GenerativeModel('gemini-1.5-pro')
model = genai.GenerativeModel('gemini-1.5-flash')
```

## Limitations

1. **AI Accuracy**: Not 100% perfect - may occasionally misclassify
2. **Scraping Limitations**: Some sites block automated scraping
3. **Processing Time**: Takes longer than non-filtered searches
4. **API Costs**: Small cost per search (though minimal)
5. **Rate Limits**: Subject to Gemini API rate limits

## Future Improvements

Potential enhancements:
- [ ] Company size database integration
- [ ] Cache AI decisions for known companies
- [ ] Batch AI requests for faster processing
- [ ] User feedback loop to improve accuracy
- [ ] Custom company size preferences
- [ ] Whitelist/blacklist functionality

## Support

If you encounter issues:
1. Check backend logs for detailed error messages
2. Verify API keys are correctly set
3. Test with AI filtering disabled
4. Check [API_REFERENCE.md](API_REFERENCE.md) for API details
5. Review [backend/README.md](../backend/README.md) for setup instructions

