import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up headless browser
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

job_query = input("Enter job role to search: ").strip().replace(" ", "%20")
url = f"https://www.mycareersfuture.gov.sg/search?search={job_query}"
driver.get(url)

wait = WebDriverWait(driver, 10)
job_data = []

try:
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="job-card-link"]')))
    job_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="job-card-link"]')

    for job_card in job_cards[:10]:
        try:
            job_url = job_card.get_attribute("href")
            title_elem = job_card.find_element(By.CSS_SELECTOR, '[data-testid="job-card__job-title"]')
            comp_elem = job_card.find_element(By.CSS_SELECTOR, '[data-testid="company-hire-info"]')
            job_title = title_elem.text.strip()
            company = comp_elem.text.strip()

            driver.execute_script("window.open(arguments[0]);", job_url)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)

            try:
                desc_elem = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="job-description"]'))
                )
                description = desc_elem.text.strip()
            except:
                description = "N/A"

            job_data.append({
                "title": job_title,
                "company": company,
                "url": job_url,
                "description": description
            })

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        except Exception as e:
            print(f"[!] Error scraping job: {e}")
            continue

finally:
    driver.quit()

if job_data:
    with open("job_listings.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "url", "description"])
        writer.writeheader()
        writer.writerows(job_data)
    print("[+] Saved to job_listings.csv")
else:
    print("[!] No job data collected.")

