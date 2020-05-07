# Posted-Job-Analysis

The idea for this project stemmed from the experiences I have had during my job search:

 - Companies now rely heavily on ATS to filter applicants. Analyzing keyword matches on a job to job basis is easy, but what are the general trends/ common skills. If you look at a macro level for a certain job/location you can ensure your template resume contains the necessary keywords, which would help limit job to job tuning.
 - Currently there is a large number of people turning to online learning. With the large amount of offerings, one of the most difficult tasks that faces students is what courses to take/ what to learn. One of the best ways to decide on what to learn is to analyze what skills companies are pursuing in applicants.
 - There is no easy way to visualize trends on the job market (ie. how many companies are hiring? / is job hiring on the rise? / what are the best geographic areas for certain jobs?) Sites such as indeed have the postings, but do not allow for analysis and visualization.

Objective:
 Create a tool that can scrape job titles, locations, companies, and descriptions off of a major job posting site and analyze/ visualize the results.

Steps:
 - Create a job scraper to pull all job titles/companies/locations
 - Add functionality to the scraper to obtain all of the job descriptions
 - Create a database to store all of the data
 - Create a notebook for easy analysis of jobs (including mapping, geographical analysis, keyword search, job title search)

Future Work:
 - geopy/Nominatim should be replaced for time-out issues
 - Create a web app for easy visualization

 Note: This project is a work in progress. Although basic functionality has been achieved, it is still rough around the edges.

# Packages:
Main scraper:
 - requests
 - bs4
 - csv
 - sqlite3
 - random
 - time
 - datetime
 - IPython.core.display
 - warnings

Description Breakdown:
 - nltk.tokenize
 - nltk.corpus

Notebook:
 - numpy
 - pandas
 - matplotlib
 - seaborn
 - certifi
 - ssl
 - geopy
