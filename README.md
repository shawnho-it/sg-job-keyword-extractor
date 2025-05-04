# SG Job Keyword Scraper

A Python-based job scraper that extracts full job descriptions from [MyCareersFuture.sg](https://www.mycareersfuture.gov.sg) based on a specified role and minimum salary. Built as a DevOps-ready project with CI/CD integration, Docker support, and AWS deployment in mind.

---

## 🎯 Project Purpose

This tool helps job seekers identify in-demand keywords and skills from real job listings. It scrapes:
- Job titles
- Companies
- Links
- Full job descriptions

The data can be used for resume tailoring, keyword extraction, or industry trend analysis.

---

## 📦 Features

- 🔎 Multi-page scraping of job listings
- 📝 Extracts full job descriptions
- 💾 Saves results to `job_listings.csv`
- 🚀 Built for automation with GitHub Actions
- 🐳 Docker-compatible
- ☁️ AWS S3 integration-ready (optional)
- 🔍 Keyword filtering handled separately by collaborator

---

## 🛠️ Tech Stack

| Tech | Purpose |
|------|---------|
| Python + Selenium | Web scraping |
| CSV | Output format |
| GitHub Actions | CI/CD automation |
| Docker | Containerization |
| AWS S3 (optional) | Storage backend |
| BeautifulSoup | HTML parsing |

---

## 🚀 How It Works

1. User enters a job role and minimum salary (or defaults can be pre-filled).
2. Script loads job search results from MyCareersFuture.
3. Navigates through each job listing and extracts:
   - Job title
   - Company
   - Job URL
   - Full job description
4. Output is saved to `job_listings.csv`.

---

## 📂 Example Output

```csv
title,company,url,description
"DevOps Engineer","TechCorp","https://www.mycareersfuture.gov.sg/...","We are looking for a DevOps Engineer to manage CI/CD pipelines..."

