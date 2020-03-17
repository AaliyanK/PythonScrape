# download webpage, grab data and clean to keep the data that we want

# airbnb.ca/robots.txt - tells us what we can and cannot scrape

# crawl delay of 30, dont overload the servers

# data requests allow us to grab HTML files

import requests  # to download HTML
from bs4 import BeautifulSoup
import pprint # cleans up print

res = requests.get('https://news.ycombinator.com/news')  # url that we want to grab data from
# USE .get() for attributes (not classes)
# print(res.text) # gives us entire html file
res2 = requests.get('https://news.ycombinator.com/news?p=2')

soup = BeautifulSoup(res.text, 'html.parser')  # Convert strings to object (list form)
soup2 = BeautifulSoup(res2.text,'html.parser')
# print(soup.find_all('div'))
# print(soup.find_all('a'))  # find all links in a list form on page
# print(soup.find_all('title'))
# print(soup.find('a'))  # finds first thing in html with a
# print(soup.find(id='score_22589657'))  #

# print(soup.select('.score'))  # list of all scores on page, use '.' for classes
# print(soup.select('#score_22589657'))  # will output information with the specific id

links = soup.select('.storylink')  # storylink is the class, we are grabbing whats inside of the tag > HERE <
subtext = soup.select('.subtext')  # grabbed votes from class

links2 = soup2.select('.storylink')
subtext2 = soup2.select('.subtext')

mega_links=links+links2
mega_subtext = subtext+subtext2

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k:k['votes'], reverse=True) # to sort dictionary and reverse makes it ascending order

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText() #grabbing all titles by enumerating
        href = links[idx].get('href',None) # grab all links, use .get for attributes
        vote = subtext[idx].select('.score')

        if len(vote): # if vote exists do this (to make sure vote is never 0)
            points = int(vote[0].getText().replace(' points',""))
            if points > 99:
                hn.append({'title':title, 'href':href, 'votes':points}) # create dictionary
    return sort_stories_by_votes(hn)



pprint.pprint(create_custom_hn(mega_links, mega_subtext))
