from requests import get
from bs4 import BeautifulSoup
import csv
from random import randint
import time
from IPython.core.display import clear_output
from warnings import warn
import datetime

# Scraper goes through pages in indeed and makes a 1 csv for company/title/location and 1 for description

# Input for job and location
job = input('Enter job: ')
while job == '':
    job = input('Enter a job not a blank: ')
location = input('Enter a location: ')
while location == '':
    location = input('Enter a location not a blank: ')

# Collecting all of the page urls
url_1 = ['https://www.indeed.ca/jobs?q={}&l={}'.format(job,location)]
scraped_job_count = 20
SCRAPED_JOB_LIMIT = 21

while scraped_job_count < SCRAPED_JOB_LIMIT:
    new_page = 'https://www.indeed.ca/jobs?q={}&l={}&start={}'.format(job,location,scraped_job_count)
    scraped_job_count += 20
    url_1.append(new_page)

# Initializing variables for monitoring
start_time = time.time()
requests = 0

# Initializing lists for scraped data
titles = []
companies = []
locations = []
job_links = []

# Beginning scraper
for url in url_1:
    response = get(url)

    # Temp wait
    time.sleep(randint(5, 10))

    # Monitoring the requests / request rate
    requests += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
    clear_output(wait=True)

    # Warning for incorrect response
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # Break setting for max amount of requests
    if requests > 72:
        warn('Number of requests was greater than expected.')
        break

    html_soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape title and company box
    job_title = html_soup.find_all('div', class_ = "title")
    job_company = html_soup.find_all('div', class_ = "sjcl")

    # Compile lists for company, location, and link to job description
    if len(job_title) == len(job_company):
        for i in range(len(job_company)):
            titles.append(job_title[i].text.lower().strip())
            companies.append(job_company[i].find('span', class_ = 'company').text.lower().strip())
            try:
                locations.append(job_company[i].find('div', class_ = 'location accessible-contrast-color-location').text.lower())
            except:
                locations.append(job_company[i].find('span', class_='location accessible-contrast-color-location').text.lower())
            job_links.append('https://www.indeed.ca' + job_title[i].find('a', href=True)['href'])

# Compiling all of the job descriptions
job_descr = []
for url in job_links:
    response2 = get(url)
    html_soup2 = BeautifulSoup(response2.text, 'html.parser')
    job_descr.append(html_soup2.find('div', class_ = 'jobsearch-jobDescriptionText').text)

id_num = [1]
for i in range(len(job_title)):
    id_num.append(id_num[i]+1)

# Creating a dict of all scraped data
comp_title_loc = zip(id_num, companies, titles, locations)

job_descr_dict = zip(id_num, job_descr)

# Creating a csvs for comp_title_loc and desc
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
with open('{}_{}_{}.csv'.format(job,location,current_date), 'w') as myfile1:
    wr = csv.writer(myfile1)
    for row in comp_title_loc:
        wr.writerow(row)
    myfile1.close()

with open('{}_{}_JobDescript_{}.csv'.format(job,location,current_date), 'w') as myfile2:
    wr2 = csv.writer(myfile2)
    for descr in job_descr:
        wr2.writerow([descr])
    myfile2.close()
