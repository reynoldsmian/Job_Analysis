# Normal scraping imports
from requests import get
from bs4 import BeautifulSoup

# Import for data export
import csv

# Import for db
import sqlite3

# Imports for scraping monitor
import random
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

    # Collect the main pages
    # Input for how many pages you want to scrape
    def url_collect(self):
        scraped_job_count = 20
        scraped_job_limit = int(input('\nHow many pages of jobs do you want to scrape? (Max 50) ')) * 20 + 1

        self.page_list = ['https://www.indeed.ca/jobs?q={}&l={}'.format(self.job, self.location)]

        while scraped_job_count < scraped_job_limit:
            new_page = 'https://www.indeed.ca/jobs?q={}&l={}&start={}'.format(self.job, self.location,
                                                                              scraped_job_count)
            scraped_job_count += 20
            self.page_list.append(new_page)

    # Main scraper for title, company, location, and links for each individual job
    # Append to title, comp, loc lists
    def title_comp_loc_scraper(self):
        # Initializing variables for monitoring
        start_time = time.time()
        requests = 0

        print('\nMain company / title / location scraper')

        # Beginning scraper
        for url in self.page_list:
            response = get(url)

            # Temp wait
            time.sleep(random.random())
            # Monitoring the requests / request rate
            requests += 1
            elapsed_time = time.time() - start_time
            print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
            clear_output(wait=True)
            # Warning for incorrect response
            if response.status_code != 200:
                warn('Request: {}; Status code: {}'.format(requests, response.status_code))
            # Break setting for max amount of requests
            if requests > 1000:
                warn('Number of requests was greater than expected.')
                break

            html_soup = BeautifulSoup(response.text, 'html.parser')

            # Scrape title and company box
            job_title = html_soup.find_all('h2', class_="title")
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

    # Secondary scraper for all of the descriptions
    # Append to descr list
    def descr_scraper(self):
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
            time.sleep(random.random())
            # Monitoring the requests / request rate
            requests += 1
            elapsed_time = time.time() - start_time
            print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
            clear_output(wait=True)
            # Warning for incorrect response
            if response2.status_code != 200:
                warn('Request: {}; Status code: {}'.format(requests, response2.status_code))
            # Break setting for max amount of requests
            if requests > 1000:
                warn('Number of requests was greater than expected.')
                break

            html_soup2 = BeautifulSoup(response2.text, 'html.parser')
            self.job_descr.append(html_soup2.find('div', class_='jobsearch-jobDescriptionText').text)

    # Zip comp, title, loc together and descr with generated id nums
    def zip_create(self):
        id_num = [1]
        for i in range(len(self.titles)):
            id_num.append(id_num[i] + 1)

        # Creating a iterable of all scraped data
        self.comp_title_loc_dict = zip(id_num, self.companies, self.titles, self.locations)
        self.job_descr_dict = zip(id_num, self.job_descr)

    def db_create(self, ):
        conn = sqlite3.connect('job_main.db')
        cur = conn.cursor()

        cur.executescript('''

            CREATE TABLE IF NOT EXISTS title_table (
                job_id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                comp_id         INTEGER,
                loc_id          INTEGER,
                title           TEXT,
                scrape_date     TEXT,
                unique(comp_id, loc_id, title)
            );

            CREATE TABLE IF NOT EXISTS comp_table (
                id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                comp           TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS loc_table (
                id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                loc            TEXT UNIQUE
            );
            
            ''')

        for entry in self.comp_title_loc_dict:
            comp = entry[1]
            title = entry[2]
            loc = entry[3]
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            cur.execute('INSERT OR IGNORE INTO comp_table (comp) VALUES ( ? )', (comp,))
            cur.execute('SELECT id FROM comp_table WHERE comp = ? ', (comp,))
            comp_id = cur.fetchone()[0]

            cur.execute('INSERT OR IGNORE INTO loc_table (loc) VALUES ( ? )', (loc,))
            cur.execute('SELECT id FROM loc_table WHERE loc = ? ', (loc,))
            loc_id = cur.fetchone()[0]

            cur.execute('''INSERT OR IGNORE INTO title_table
                (comp_id, loc_id, title, scrape_date) VALUES ( ?,?,?,? )''', (comp_id, loc_id, title, date))
            cur.execute('SELECT job_id FROM title_table WHERE title = ? ', (title,))

            conn.commit()

    # Creating csv for title / comp / loc
    def csv_create_title_comp_loc(self):
        with open('scrape_csvs/{}_{}_{}.csv'.format(self.job, self.location, self.current_date), 'w') as myfile1:
            wr = csv.writer(myfile1)
            for row in self.comp_title_loc_dict:
                wr.writerow(row)
            myfile1.close()

    # Creating csv for descr
    def csv_create_descr(self):
        with open('scrape_csvs/{}_{}_JobDescript_{}.csv'.format(self.job, self.location, self.current_date), 'w') as myfile2:
            wr2 = csv.writer(myfile2)
            for descr in self.job_descr:
                wr2.writerow([descr])
            myfile2.close()

    # Overall for title, comp, and loc
    def scrape_export_title_comp_loc(self):
        self.url_collect()
        self.title_comp_loc_scraper()
        self.zip_create()
        self.db_create()
        self.zip_create()
        self.csv_create_title_comp_loc()

    # Inclusion of the job description
    def scrape_export_title_comp_loc_descr(self):
        self.url_collect()
        self.title_comp_loc_scraper()
        self.descr_scraper()
        self.zip_create()
        self.csv_create_title_comp_loc()
        self.csv_create_descr()
