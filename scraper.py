import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_scraper_and_return_data(job_query, min_salary):
    job_query = job_query.strip().replace(" ", "%20")
    base_url = f"https://www.mycareersfuture.gov.sg/search?search={job_query}"
    if min_salary:
        base_url += f"&salary={min_salary}"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    driver.get(base_url)
    job_data = []
    total_jobs = 0
    page_num = 1
    max_jobs = 3
    logs = []

    while total_jobs < max_jobs:
        msg = f"🔎 Scraping page {page_num}..."
        logs.append(msg)
        print(msg)

        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="job-card-link"]')))
            job_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="job-card-link"]')
        except Exception as e:
            msg = f"❌ No job cards found: {e}"
            logs.append(msg)
            print(msg)
            break

        for job_card in job_cards:
            if total_jobs >= max_jobs:
                break
            try:
                job_url = job_card.get_attribute("href")
                job_title = job_card.find_element(By.CSS_SELECTOR, '[data-testid="job-card__job-title"]').text.strip()
                company = job_card.find_element(By.CSS_SELECTOR, '[data-testid="company-hire-info"]').text.strip()

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

                msg = f"✅ Collected: {job_title} at {company}"
                logs.append(msg)
                print(msg)

                total_jobs += 1
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
            except Exception as e:
                msg = f"❌ Error scraping job: {e}"
                logs.append(msg)
                print(msg)
                continue

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="pagination-button--❯"]')
            if "disabled" in next_button.get_attribute("class"):
                logs.append("ℹ️ No more pages.")
                print("ℹ️ No more pages.")
                break
            next_button.click()
            page_num += 1
            time.sleep(2)
        except:
            logs.append("⚠️ No next button found.")
            print("⚠️ No next button found.")
            break

    driver.quit()

    if job_data:
        with open("job_listings.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "company", "url", "description"])
            writer.writeheader()
            writer.writerows(job_data)
        logs.append("📅 Saved to job_listings.csv")
        print("📅 Saved to job_listings.csv")
    else:
        logs.append("❌ No job data collected.")
        print("❌ No job data collected.")

    return logs, job_data

if __name__ == "__main__":
    job_role = input("Enter job role to search: ").strip()
    min_salary = input("Enter minimum salary (or leave blank to skip): ").strip()
    logs, jobs = run_scraper_and_return_data(job_role, min_salary)

