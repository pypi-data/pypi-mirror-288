# linkedin_search_job/scraper.py

import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def scrape_jobs(job_keyword="", location="", f_WT="", f_JT="", f_E="", f_SB2="", start=""):
    initial_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={job_keyword}&location={location}&f_TPR=&f_WT={f_WT}&f_JT={f_JT}&f_E={f_E}&f_SB2={f_SB2}&start={start}"
    encoded_url = urllib.parse.quote(initial_url, safe=':/?=&')
    
    response = requests.get(encoded_url)
    time.sleep(7)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    job_listings = []
    
    li_tags = soup.find_all('li')
    for job in li_tags:
        title = job.find('h3', class_='base-search-card__title').get_text(strip=True)
        company = job.find('h4', class_='base-search-card__subtitle').get_text(strip=True)
        location = job.find('span', class_='job-search-card__location').get_text(strip=True)
        job_link = job.find('a', class_='base-card__full-link')['href']
        
        job_listings.append({
            'title': title,
            'company': company,
            'location': location,
            'job_link': job_link
        })
        
    return job_listings

def main():
    # Example usage with default parameters
    jobs = scrape_jobs()
    for job in jobs:
        print(f"Job Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Job Link: {job['job_link']}")
        print('---')

if __name__ == "__main__":
    main()
