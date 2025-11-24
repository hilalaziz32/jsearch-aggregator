"""
Test script for AI filtering functionality

This script demonstrates how the AI filtering works by testing it on sample job data.
"""

import sys
from ai_filter import filter_job_with_ai, analyze_with_gemini, fuzzy_match_yes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sample job data for testing
SAMPLE_JOBS = [
    {
        "job_id": "test1",
        "job_title": "Software Engineer",
        "employer_name": "Google",
        "employer_company_type": "Large Corporation",
        "employer_website": "https://google.com",
        "job_location": "Mountain View, CA",
        "job_description": "Join Google's engineering team to build products used by billions.",
        "job_apply_link": "https://careers.google.com/jobs/example",
        "job_naics_name": "Internet Publishing and Broadcasting and Web Search Portals"
    },
    {
        "job_id": "test2",
        "job_title": "Frontend Developer",
        "employer_name": "StartupXYZ",
        "employer_company_type": "Small Business",
        "employer_website": "https://startupxyz.com",
        "job_location": "Austin, TX",
        "job_description": "Join our small team of 15 people building innovative SaaS solutions. We're a small business with under 50 employees.",
        "job_apply_link": "https://startupxyz.com/careers",
        "job_naics_name": "Custom Computer Programming Services"
    },
    {
        "job_id": "test3",
        "job_title": "Python Developer",
        "employer_name": "Local Tech Solutions",
        "employer_company_type": "Medium Business",
        "employer_website": "https://localtechsolutions.com",
        "job_location": "Portland, OR",
        "job_description": "Medium-sized consulting firm looking for Python developer. We have 200 employees across 3 offices.",
        "job_apply_link": "https://localtechsolutions.com/jobs",
        "job_naics_name": "Computer Systems Design Services"
    },
    {
        "job_id": "test4",
        "job_title": "Senior Engineer",
        "employer_name": "Amazon",
        "employer_company_type": "Public Company",
        "employer_website": "https://amazon.com",
        "job_location": "Seattle, WA",
        "job_description": "Amazon is looking for talented engineers to join AWS team.",
        "job_apply_link": "https://amazon.jobs/example",
        "job_naics_name": "Electronic Shopping"
    },
    {
        "job_id": "test5",
        "job_title": "Full Stack Developer",
        "employer_name": "TechBoutique LLC",
        "employer_company_type": "Small Business",
        "employer_website": "https://techboutique.com",
        "job_location": "Denver, CO",
        "job_description": "Boutique software agency with 30 employees seeking full stack developer. Small business focused on custom solutions.",
        "job_apply_link": "https://techboutique.com/careers",
        "job_naics_name": "Custom Computer Programming Services"
    },
    {
        "job_id": "test6",
        "job_title": "Backend Engineer",
        "employer_name": "MegaTech Solutions",
        "employer_company_type": "Large Enterprise",
        "employer_website": "https://megatechsolutions.com",
        "job_location": "Boston, MA",
        "job_description": "MegaTech Solutions is a rapidly growing company with 800 employees across 15 offices worldwide.",
        "job_apply_link": "https://megatechsolutions.com/careers",
        "job_naics_name": "Custom Computer Programming Services"
    }
]


def test_fuzzy_matching():
    """Test fuzzy matching function"""
    print("\n" + "="*60)
    print("Testing Fuzzy Matching")
    print("="*60 + "\n")
    
    test_cases = [
        ("yes", True),
        ("Yes", True),
        ("YES", True),
        ("yess", True),
        ("yep", False),
        ("yeah", False),
        ("no", False),
        ("No", False),
        ("nope", False),
        ("maybe", False),
    ]
    
    for response, expected in test_cases:
        result = fuzzy_match_yes(response)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{response}' -> {result} (expected: {expected})")


def test_ai_analysis():
    """Test AI analysis on sample jobs"""
    print("\n" + "="*60)
    print("Testing AI Analysis on Sample Jobs")
    print("="*60 + "\n")
    
    for idx, job in enumerate(SAMPLE_JOBS, 1):
        print(f"\n{'='*60}")
        print(f"Test {idx}/{len(SAMPLE_JOBS)}")
        print(f"{'='*60}")
        
        # Test without scraping (faster)
        should_keep = filter_job_with_ai(job, scrape_links=False)
        
        result = "✅ KEPT" if should_keep else "❌ REMOVED"
        print(f"\nFinal Decision: {result}\n")


def test_single_job():
    """Test AI filtering on a single job"""
    print("\n" + "="*60)
    print("Testing Single Job with Scraping")
    print("="*60 + "\n")
    
    # Test on the small business job (should be kept)
    job = SAMPLE_JOBS[1]  # StartupXYZ
    
    print("Testing job:")
    print(f"  Title: {job['job_title']}")
    print(f"  Company: {job['employer_name']}")
    print(f"  Type: {job['employer_company_type']}")
    print()
    
    should_keep = filter_job_with_ai(job, scrape_links=True)
    
    if should_keep:
        print("\n✅ SUCCESS: Job was kept (Small/Medium Business detected)")
    else:
        print("\n❌ FAILED: Job was removed (might be misclassified)")


def main():
    """Main test function"""
    print("\n" + "🤖"*30)
    print(" " * 20 + "AI FILTER TEST SUITE")
    print("🤖"*30 + "\n")
    
    if len(sys.argv) > 1:
        test_mode = sys.argv[1]
        
        if test_mode == "fuzzy":
            test_fuzzy_matching()
        elif test_mode == "single":
            test_single_job()
        elif test_mode == "all":
            test_ai_analysis()
        else:
            print(f"Unknown test mode: {test_mode}")
            print("Available modes: fuzzy, single, all")
    else:
        # Run all tests
        print("Running all tests...\n")
        test_fuzzy_matching()
        test_ai_analysis()
    
    print("\n" + "="*60)
    print("Tests Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

