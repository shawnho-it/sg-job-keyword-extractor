from scraper import run_scraper

# Call it with any role + salary you want
result = run_scraper("devops engineer", "8000")

if result:
    print(f"[TEST PASS] Scraped data saved to: {result}")
else:
    print("[TEST FAIL] No data was saved.")

