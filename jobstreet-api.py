import threading
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import summarizer
import time

url = "https://sg.jobstreet.com/api/jobsearch/v5/search"

job_listings = []

def get_job_url():
    user_input = input("Search Job Title: ")
    print("You entered:", user_input)
    print()

    y = user_input
    for x in range(0, 1):
        querystring = {
            "siteKey": "SG-Main",
            "sourcesystem": "houston",
            "userqueryid": "36d7d8b41696017af4c442da6bbf62e8-8346603",
            "userid": "f3e02263-01c2-473d-bebf-1f55ebcd98e7",
            "usersessionid": "f3e02263-01c2-473d-bebf-1f55ebcd98e7",
            "eventCaptureSessionId": "f3e02263-01c2-473d-bebf-1f55ebcd98e7",
            "page": f"{x}",
            "seekSelectAllPages": "true",
            "keywords": f"{y}",
            "pageSize": "48",
            "include": "seodata",
            "locale": "en-SG",
            "solId": "d48abeb0-26eb-48d7-ba7a-dcc201eb484a",
            "isStandOut": "True"
        }

        headers = {
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "referer": "https://sg.jobstreet.com/jobs",
            "x-seek-checksum": "12a140d5",
        }

        cookies = {
            "JobseekerSessionId": "f3e02263-01c2-473d-bebf-1f55ebcd98e7",
            "JobseekerVisitorId": "f3e02263-01c2-473d-bebf-1f55ebcd98e7",
            "sol_id": "d48abeb0-26eb-48d7-ba7a-dcc201eb484a"
        }

        response = requests.get(url, headers=headers, cookies=cookies, params=querystring)

        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            return

        for index, item in enumerate(data.get('data', [])):
            job_listing = {
                'Company Name': item.get('advertiser', {}).get('description', 'N/A'),
                'Company ID': item.get('advertiser', {}).get('id', 'N/A'),
                'Job ID': item.get('id', 'N/A'),
                'Company Area': item.get('area', 'N/A'),
                'Company Logo': item.get('branding', {}).get('assets', {}).get('logo', {}).get('strategies', {}).get('jdpLogo', 'N/A'),
                'Company Classification': item.get('classification', {}).get('description', 'N/A'),
                'Listing Date': item.get('listingDate', 'N/A'),
                'Job Title': item.get('title', 'N/A'),
                'Job Salary': item.get('salary', 'N/A'),
                'Job Teaser': item.get('teaser', 'N/A'),
                'Job Type': item.get('workType', 'N/A')
            }
            job_listings.append(job_listing)

def getParsedWebpage(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/93.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    page = requests.get(url, headers=headers)
    if page.status_code != 200:
        return 'error'
    return BeautifulSoup(page.content, 'html.parser')

def get_job_details():
    details_dict = {}
    for job in job_listings:
        print(f"Parsing Job: {job.get('Job Title')}")
        job_id = job.get('Job ID')
        job_url = f"https://www.jobstreet.com.sg/job/{job_id}"
        web = getParsedWebpage(job_url)
        if web == 'error':
            continue
        specific_div = web.find('div', {'data-automation': 'jobAdDetails'})
        sections = [section.text.strip() for section in specific_div.find_all(['p', 'li'])] if specific_div else []
        details_dict[job_id] = {**job, 'Job Details Sections': sections}
    return details_dict

def search_job():
    get_job_url()
    details = get_job_details()
    description_all = []
    limit = 30
    for i, job in enumerate(job_listings[:limit]):
        print(f"Summarizing Job {i+1}: {job['Job Title']}")
        time.sleep(0.2)
        job_details = details.get(job['Job ID'], {}).get('Job Details Sections', [])
        description_all.extend(job_details)
    summary_all_string = ' '.join(description_all)
    sort = summarizer.sort_by_trend(summary_all_string)
    print(sort)
search_job()
print("=" * 60)
