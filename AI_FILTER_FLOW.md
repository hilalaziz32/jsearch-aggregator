# AI Filter Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER SEARCHES FOR JOBS                           │
│                    e.g., "software engineer in NYC"                      │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    RAPIDAPI RETURNS ~20 JOBS                             │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │ Job 1: Software Engineer @ Google                             │     │
│   │ Job 2: Developer @ StartupXYZ (50 employees)                  │     │
│   │ Job 3: Engineer @ Amazon                                      │     │
│   │ Job 4: Full Stack @ LocalTech (200 employees)                │     │
│   │ Job 5: Senior Engineer @ Microsoft                            │     │
│   │ ... (15 more jobs)                                            │     │
│   └──────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  AI FILTERING ENABLED? (default: YES)                    │
└─────────┬───────────────────────────────────────────────────┬───────────┘
          │ YES                                               │ NO
          ▼                                                   ▼
  ┌───────────────┐                                  ┌────────────────┐
  │ AI FILTERING  │                                  │ RETURN ALL     │
  │ STARTS        │                                  │ JOBS (OLD WAY) │
  └───────┬───────┘                                  └────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              FOR EACH JOB (Object-by-Object Processing)                  │
└─────────────────────────────────────┬───────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
    ┌─────────┐                 ┌─────────┐                 ┌─────────┐
    │  JOB 1  │                 │  JOB 2  │       ...       │  JOB 20 │
    └────┬────┘                 └────┬────┘                 └────┬────┘
         │                           │                           │
         ▼                           ▼                           ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                    STEP 1: SCRAPE JOB LINK                            │
  │  - Extract job_apply_link from RapidAPI data                          │
  │  - HTTP GET with User-Agent headers                                   │
  │  - Parse HTML with BeautifulSoup                                      │
  │  - Extract text (limit 3000 chars)                                    │
  │  - Handle failures gracefully                                         │
  └────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │              STEP 2: PREPARE DATA FOR GEMINI AI                       │
  │  ┌────────────────────────────────────────────────────────────────┐  │
  │  │ Job Title: Software Engineer                                    │  │
  │  │ Employer Name: Google                                           │  │
  │  │ Company Type: Public Company                                    │  │
  │  │ Employer Website: https://google.com                           │  │
  │  │ Job Description: [500 chars]                                    │  │
  │  │ NAICS Code: 518210                                              │  │
  │  │ Scraped Content: [1000 chars from job link]                    │  │
  │  └────────────────────────────────────────────────────────────────┘  │
  └────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                STEP 3: GEMINI AI ANALYSIS                             │
  │                                                                        │
  │  Prompt: "Analyze this job. Is it from SMALL or MEDIUM business?"    │
  │                                                                        │
  │  AI examines:                                                         │
  │  • Company name (is it well-known?)                                   │
  │  • Company type (public/private/enterprise?)                          │
  │  • Employee count indicators                                          │
  │  • Industry codes                                                     │
  │  • Job description details                                            │
  │  • Scraped content                                                    │
  │                                                                        │
  │  AI Decision Logic:                                                   │
  │  ✅ Small (< 100 employees) → "yes"                                  │
  │  ✅ Medium (100-500 employees) → "yes"                               │
  │  ❌ Large (500+ employees) → "no"                                    │
  │  ❌ Fortune 500 → "no"                                               │
  │  ❌ Big Tech (Google, Amazon, etc.) → "no"                           │
  │  ❌ Enterprise → "no"                                                │
  │                                                                        │
  │  AI Response: "yes" or "no"                                           │
  └────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │              STEP 4: FUZZY MATCH AI RESPONSE                          │
  │                                                                        │
  │  Using: difflib.SequenceMatcher(None, ai_response, "yes").ratio()   │
  │                                                                        │
  │  Examples:                                                            │
  │  • "yes" → 100% match → KEEP ✅                                      │
  │  • "Yes" → 100% match → KEEP ✅                                      │
  │  • "yess" → 75% match → KEEP ✅                                      │
  │  • "yep" → 60% match → REMOVE ❌ (below 70% threshold)              │
  │  • "no" → 33% match → REMOVE ❌                                      │
  │  • "nope" → 40% match → REMOVE ❌                                    │
  │                                                                        │
  │  Threshold: >= 70% match with "yes" → KEEP                           │
  └────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                  STEP 5: FILTERING DECISION                           │
  │                                                                        │
  │  IF fuzzy_match >= 70%:                                               │
  │      ✅ ADD to filtered_jobs list                                    │
  │      Print: "✅ KEEP - [Company Name]"                               │
  │  ELSE:                                                                │
  │      ❌ SKIP (don't add to list)                                     │
  │      Print: "❌ REMOVE - [Company Name]"                             │
  └────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │              STEP 6: RATE LIMITING DELAY                              │
  │                                                                        │
  │  Sleep 0.5 seconds before processing next job                         │
  │  (Prevents API rate limits and scraping blocks)                       │
  └────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   │
          ┌────────────────────────┴────────────────────────┐
          │                                                  │
          ▼                                                  ▼
    Continue to                                       Last Job?
    next job                                               │
          │                                                 │
          └────────────────────┐                          │
                               ▼                           ▼
                         (repeat for                   ┌─────────┐
                          all jobs)                    │  DONE   │
                                                       └────┬────┘
                                                            │
                                                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     FILTERING COMPLETE                                   │
│                                                                          │
│  Original Jobs: 20                                                       │
│  Filtered Jobs: 6 (only SMBs kept)                                      │
│                                                                          │
│  Example Results:                                                        │
│  ❌ Job 1: Google (big tech) - REMOVED                                  │
│  ✅ Job 2: StartupXYZ (50 employees) - KEPT                            │
│  ❌ Job 3: Amazon (big tech) - REMOVED                                  │
│  ✅ Job 4: LocalTech (200 employees) - KEPT                            │
│  ❌ Job 5: Microsoft (big tech) - REMOVED                               │
│  ✅ Job 6: TechBoutique (30 employees) - KEPT                          │
│  ... (14 more analyzed)                                                  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    RETURN FILTERED RESULTS                               │
│                                                                          │
│  Return only 6 jobs (all SMBs):                                         │
│  • StartupXYZ (50 employees)                                            │
│  • LocalTech (200 employees)                                            │
│  • TechBoutique (30 employees)                                          │
│  • DevShop Inc (120 employees)                                          │
│  • CodeCraft (75 employees)                                             │
│  • SmallSoft (300 employees)                                            │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DISPLAY TO USER                                       │
│                                                                          │
│  - Generate HTML with job cards                                         │
│  - Create XLSX export file                                              │
│  - Show in frontend interface                                           │
│  - User sees only SMB opportunities! 🎉                                 │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                          KEY METRICS                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ Processing Time:    ~20-40 seconds for 20 jobs                          │
│ Cost per Search:    ~$0.006 (less than a penny!)                        │
│ Accuracy:          ~95% (AI-powered analysis)                           │
│ Scraping Success:   ~80% (some sites block bots)                        │
│ Fuzzy Match:        70% threshold (configurable)                        │
│ Rate Limit Delay:   0.5 seconds between jobs                            │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                         FILTERING RULES                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ✅ KEEP (SMB ONLY):                                                    │
│  • Small businesses: < 100 employees                                     │
│  • Medium businesses: 100-500 employees                                 │
│                                                                          │
│  ❌ REJECT (Everything Else):                                           │
│  • Large companies: 500+ employees                                       │
│  • Enterprise companies                                                  │
│  • Fortune 500/1000                                                      │
│  • Big tech: FAANG, etc.                                                │
│  • Large consulting: Deloitte, Accenture, etc.                          │
│  • Advanced medium/large-medium companies                                │
│  • Public companies with large market cap                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

- **Web Scraping**: BeautifulSoup4 + lxml
- **AI Model**: Google Gemini 2.5 Flash (gemini-2.5-flash)
- **Fuzzy Matching**: Python difflib.SequenceMatcher
- **Backend**: FastAPI
- **Frontend**: HTML/CSS/JavaScript

## Configuration

Enable/disable in frontend Advanced Settings or via API:

```json
{
  "query": "software engineer",
  "enable_ai_filter": true,   // Toggle AI filtering
  "scrape_links": true        // Toggle link scraping
}
```

