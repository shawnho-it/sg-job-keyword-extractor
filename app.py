# scraper.py
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_scraper(job_query: str, min_salary: str) -> str:
    # Clean inputs
    job_query = job_query.strip().replace(" ", "%20")
    base_url = f"https://www.mycareersfuture.gov.sg/search?search={job_query}&salary={min_salary}"

    # Set up headless browser
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(base_url)

    job_data = []
    page_num = 1
    total_jobs = 0

    while True:
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="job-card-link"]')))
            job_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="job-card-link"]')
        except:
            break

        for job_card in job_cards:
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

                total_jobs += 1

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)

            except Exception:
                continue

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="pagination-button--❯"]')
            if "disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
            page_num += 1
            time.sleep(2)
        except:
            break

    driver.quit()

    if job_data:
        output_file = "job_listings.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "company", "url", "description"])
            writer.writeheader()
            writer.writerows(job_data)
        return output_file
    else:
        return ""

