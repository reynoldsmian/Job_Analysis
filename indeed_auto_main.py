# Normal scraping imports
from requests import get
from bs4 import BeautifulSoup

# Import for data export
import csv

# Imports for scraping monitor
from random import randint
import time
import datetime
from IPython.core.display import clear_output
from warnings import warn


# Scraper goes through pages in indeed and makes a 1 csv for company/title/location and 1 for description

class web_scraper:
    def __init__(self, job='Engineer', location='Canada'):
        self.job = job
        self.location = location

        self.page_list = []
        self.job_link_list = []

        self.titles = []
        self.companies = []
        self.locations = []
        self.job_links = []
        self.job_descr = []

        self.comp_title_loc_dict = {}
        self.job_descr_dict = {}

        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")


    def url_collect(self):
        SCRAPED_JOB_COUNT = 20
        scraped_job_limit = int(input('\nHow many pages of jobs do you want to scrape? ')) * 20 + 1

        self.page_list = ['https://www.indeed.ca/jobs?q={}&l={}'.format(self.job, self.location)]

        while SCRAPED_JOB_COUNT < scraped_job_limit:
            new_page = 'https://www.indeed.ca/jobs?q={}&l={}&start={}'.format(self.job, self.location, SCRAPED_JOB_COUNT)
            SCRAPED_JOB_COUNT += 20
            self.page_list.append(new_page)

    def title_comp_loc_scraper(self):
        # Initializing variables for monitoring
        start_time = time.time()
        requests = 0

        print('\nMain company / title / location scraper')

        # Beginning scraper
        for url in self.page_list:
            response = get(url)

            # Temp wait
            time.sleep(randint(1, 2))
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
            job_title = html_soup.find_all('div', class_="title")
            job_company = html_soup.find_all('div', class_="sjcl")

            # Compile lists for company, location, and link to job description
            if len(job_title) == len(job_company):
                for i in range(len(job_company)):
                    self.titles.append(job_title[i].text.lower().strip())
                    self.companies.append(job_company[i].find('span', class_='company').text.lower().strip())
                    try:
                        self.locations.append(job_company[i].find('div',
                                                             class_='location accessible-contrast-color-location').text.lower())
                    except:
                        self.locations.append(job_company[i].find('span',
                                                             class_='location accessible-contrast-color-location').text.lower())
                    self.job_link_list.append('https://www.indeed.ca' + job_title[i].find('a', href=True)['href'])

    def descr_scraper(self):
        # Compiling all of the job descriptions

        check = input('\n{} jobs will be scraped. Continue? (y/n) '.format(len(self.job_link_list)))
        if check == 'n':
            raise SystemExit

        # Initializing variables for monitoring
        start_time = time.time()
        requests = 0

        print('\nJob description scraper')

        for url in self.job_link_list:
            response2 = get(url)

            # Temp wait
            time.sleep(randint(1,2))
            # Monitoring the requests / request rate
            requests += 1
            elapsed_time = time.time() - start_time
            print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
            clear_output(wait=True)
            # Warning for incorrect response
            if response2.status_code != 200:
                warn('Request: {}; Status code: {}'.format(requests, response2.status_code))
            # Break setting for max amount of requests
            if requests > 72:
                warn('Number of requests was greater than expected.')
                break

            html_soup2 = BeautifulSoup(response2.text, 'html.parser')
            self.job_descr.append(html_soup2.find('div', class_='jobsearch-jobDescriptionText').text)

    def dict_create(self):
        id_num = [1]
        for i in range(len(self.titles)):
            id_num.append(id_num[i] + 1)

        # Creating a dict of all scraped data
        self.comp_title_loc_dict = zip(id_num, self.companies, self.titles, self.locations)
        self.job_descr_dict = zip(id_num, self.job_descr)

    def csv_create_title_comp_loc(self):
        # Creating csv for title / comp / loc
        with open('{}_{}_{}.csv'.format(self.job, self.location, self.current_date), 'w') as myfile1:
            wr = csv.writer(myfile1)
            for row in self.comp_title_loc_dict:
                wr.writerow(row)
            myfile1.close()

    def csv_create_descr(self):
        # Creating csv for descr
        with open('{}_{}_JobDescript_{}.csv'.format(self.job, self.location, self.current_date), 'w') as myfile2:
            wr2 = csv.writer(myfile2)
            for descr in self.job_descr:
                wr2.writerow([descr])
            myfile2.close()

    def scrape_export_title_comp_loc(self):
        self.url_collect()
        self.title_comp_loc_scraper()
        self.dict_create()
        self.csv_create_descr()

    def scrape_export_title_comp_loc_descr(self):
        self.url_collect()
        self.title_comp_loc_scraper()
        self.descr_scraper()
        self.dict_create()
        self.csv_create_title_comp_loc()
        self.csv_create_descr()

search1 = web_scraper('Engineer','Canada')
search1.scrape_export_title_comp_loc_descr()
