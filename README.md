# Posted-Job-Analysis

Idea behind the project:
Job Description Keyword Search
 - Currently there is a large number of people turning to online learning. This trend will slow, but continue once social distancing ends. With the large amount of offerings, one of the most difficult tasks that faces students is what courses to take/ what to learn. One of the best ways to decide on what to learn is to analyze what skills companies are pursuing in applicants. This project gives a tool to compare how often skills are mentioned across the job market.

 General Analysis:
 - There is no easy way to visualize trends on the job market. Sites such as indeed have the postings, but do not allow for analysis and visualization. This project will allow visualization of where the jobs are located, what companies are hiring, and what positions are needed.

 Steps:
 - Create a job scraper to pull all job titles/companies/locations
 - Add functionality to the scraper to obtain all of the job descriptions
 - Create a notebook for easy analysis of jobs

Future Work:
 - Add database functionality to store jobs/ track trends over time
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
