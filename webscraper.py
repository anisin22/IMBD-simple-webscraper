from os import name
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
from random import randint
from warnings import warn
import os

movie_names = []
movie_years = []
movie_imdb_ratings = []
movie_metascores = []
movie_votes = []

def scrape(start_year, end_year):

    years = [str(i) for i in range(start_year,end_year)]
    

    start_time = time()
    requests = 0

    for year in years:

        response = get('https://www.imdb.com/search/title?release_date=' + year + '&sort=num_votes,desc&page=2', headers = {"Accept-Language": "en-US, en;q=0.5"})

        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))

        sleep(randint(5,8))
        

        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        html_soup = BeautifulSoup(response.text, 'html.parser')
        movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

        for container in movie_containers:
            
            name = container.h3.a.text
            movie_names.append(name)

            year = container.h3.find('span', class_ = 'lister-item-year').text
            movie_years.append(year)

            imdb = container.strong.text
            movie_imdb_ratings.append(imdb)

            if container.find('div', class_ = 'ratings-metascore') is not None:
                metascore = container.find('span', class_ = 'metascore').text
                movie_metascores.append((metascore))
            else:
                movie_metascores.append('NULL')

            vote = container.find('span', attrs = {'name':'nv'}).text
            movie_votes.append((vote))

        os.system('cls')

def get_input():
    start_year = input("Enter start year of when you want to start scraping movies from: ")
    while start_year.isdigit() == False or len(start_year) != 4 or int(start_year) < 1885 or int(start_year) > 2050:
        start_year = input("Enter start year of when you want to start scraping movies from: ")
    start_year = int(start_year)
    
    end_year = input("Enter the end year of when you want to stop scraping movies from: ")
    while end_year.isdigit() == False or len(end_year) != 4 or int(end_year) < 1885 or int(end_year) > 2050:
        end_year = input("Enter the end year of when you want to stop scraping movies from: ")
    end_year = int(end_year) + 1

    return start_year, end_year

def print_scraped():
    for i in range(len(movie_names)):
        print("Movie Name: " + movie_names[i])
        print("Year Movie was Released: " + movie_years[i])
        print("IMBD Score: " + movie_imdb_ratings[i])
        print("MetaScore: " + movie_metascores[i])
        print("Total Votes on IMBD: " + movie_votes[i])
        print('\n' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' + '\n') 

def main():
    start, end = get_input()
    scrape(start,end)
    print_scraped()

if __name__ == "__main__":
    main()