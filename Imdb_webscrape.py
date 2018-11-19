###############################################################################
#
#                    WEB SCRAPING IN PYTHON IMBD WEBSITE
#
#
# REF: https://www.imdb.com/
# 
#
###############################################################################

#Scrape movie detials from imdb website and store as csv file

#Download the website
import requests
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep,time
from random import randint
from IPython.core.display import clear_output

#WEBSITE AND ITS URLS TO BE SCRAPED
WebsiteURL = "https://www.imdb.com/"
#ScrapeURL =  "/search/title?release_date=2017&sort=num_votes,desc&page=1"
ScrapeURL_1 = "/search/title?release_date="
ScrapeURL_2 ="&sort=num_votes,desc&page="

# Lists to store the scraped data in
Movienames = []
Movieyears = []
Movieimdb_ratings = []
Movemetascores = []
Movievotes = []
Moviecertificate = []
Movieshowtime = []
Moviegenre =[]
MovieSummary = []
pages = []
years_url =[]

def fill_No_Values(x):
       if pd.notnull(x):
              x = x
       else:
              x='NA'
       return x


# SCRAPE FOR MULTIPLE YEARS AND MULTIPLE PAGES
pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2010,2018)]


# Preparing the monitoring of the loop
start_time = time()
req = 0

# For every year in the interval 2000-2017
for year_url in years_url:
       # For every page in the interval 1-4
       for page in pages:
              # Make a get request
              url = requests.get(WebsiteURL+ScrapeURL_1+ year_url +ScrapeURL_2 + page, headers = {"Accept-Language": "en-US, en;q=0.5"})
              # Monitor the requests
              req = req + 1
              elapsed_time = time() - start_time
              print('Request:{}; Frequency: {} requests/s'.format(req, req/elapsed_time))
              clear_output(wait = True)#wait = True
              if url.status_code == 200:
                     print("{} downloaded successfully".format(str(WebsiteURL+ScrapeURL_1+ year_url +ScrapeURL_2 + page)))
              else:
                     print ("Some error occured in downloading your webpage {}".format(str(WebsiteURL+ScrapeURL_1+ year_url +ScrapeURL_2 + page)))        
              # Parse the content of the request with BeautifulSoup
              url_soup = BeautifulSoup(url.text,'html.parser')
              movie_containers = url_soup.find_all('div', class_ = 'lister-item mode-advanced')
              # Extract data from individual movie container
              for container in movie_containers:
                     # If the movie has Metascore, then extract:
                     if container.find('div', class_ = 'ratings-metascore') is not None:
                            # The name
                            name = container.h3.a.text
                            Movienames.append(fill_No_Values(name))
                     
                            # The year
                            year = container.h3.find('span', class_ = 'lister-item-year').text
                            Movieyears.append(fill_No_Values(year))
                     
                            # The IMDB rating
                            imdb = float(container.strong.text)
                            Movieimdb_ratings.append(fill_No_Values(imdb))
                     
                            # The Metascore
                            m_score = container.find('span', class_ = 'metascore').text
                            Movemetascores.append(fill_No_Values(int(m_score)))
                     
                            # The number of votes
                            vote = container.find('span', attrs = {'name':'nv'})['data-value']
                            Movievotes.append(fill_No_Values(int(vote)))
                             
                            #The Certificate of the movie
                            certificate = container.p.find('span', class_ = 'certificate')
                            if certificate:
                                   certificate=certificate.text
                            else:
                                   certificate ='NA'
                                   
                            Moviecertificate.append(fill_No_Values(certificate))
                             
                            #The show time of the movie
                            showtime = container.p.find('span', class_ = 'runtime').text
                            Movieshowtime.append(fill_No_Values(int(showtime.replace(" min",''))))
                             
                            #The show time of the movie
                            genre = container.p.find('span', class_ = 'genre').text
                            genre=str(genre)
                            genre=genre.replace("\n",'')
                            Moviegenre.append(fill_No_Values(genre))
                             
                            # Go to individual Movie page get extra page
                            for lnk in container.h3.find_all('a'):
                                   MoviePage = lnk.get('href')
                                   movieurl = WebsiteURL+lnk.get('href')
                                   MovieDetails = requests.get(movieurl)
                                   movie_html = BeautifulSoup(MovieDetails.content,'html.parser')
                                   summary = movie_html.find('div',class_="summary_text").text
                                   summary = str(summary)
                                   summary=summary.replace("\n",'')
                                   summary=summary.lstrip()
                                   MovieSummary.append(fill_No_Values(summary))

            




imdb_data= pd.DataFrame({'movie': Movienames,
                       'year': Movieyears,
                       'imdb': Movieimdb_ratings,
                       'metascore': Movemetascores,
                       'votes': Movievotes,
                       'certificate':Moviecertificate,
                       'showtime(mins)':Movieshowtime,
                       'genre':Moviegenre,
                       'summary':MovieSummary})

       
imdb_data.to_csv("IMDB_SCRAPE_DATA.csv", encoding='utf-8', index=False)



