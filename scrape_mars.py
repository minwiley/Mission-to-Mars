## Step 2 - MongoDB and Flask Application
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
# * Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
# * Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
#   * Store the return value in Mongo as a Python dictionary.
# * Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# * Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.

# dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

import requests
import pandas as pd
import time
import datetime
import os
import pymongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
	executable_path = {'executable_path': 'C:\Program Files\chromedriver\chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=False)

mars = {}

def scrape_mars():
	try:
    	browser = init_browser()
	    url = 'https://mars.nasa.gov/news/'
		browser.visit(url)

		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')

		mars_title = soup.find('div', class_='content_title').find('a').text
		mars_p = soup.find('div', class_='article_teaser_body').text

		mars['mars_title'] = mars_title
		mars['mars_p'] = mars_p

		return mars

	finally:
		browser.quit()

def scrape_img():
	try:
		browser = init_browser()
		jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
		browser.visit(jpl_url)

		jpl_html = browser.html
		jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

		image_full = jpl_soup.find("img", class_="fancybox-image")["src"]
		image_url = (f"https://jpl.nasa.gov{image_full}")
		print(f'image url: {image_url}')

		mars['image_url'] = image_url

		return mars

	finally:
		browser.quit()

def scrape_weather():
	try:
		browser = init_browser()
		mars_weather = 'https://twitter.com/marswxreport?lang=en'
		browser.visit(mars_weather)
		mars_weather_html = browser.html
		mars_soup = BeautifulSoup(mars_weather_html,'html.parser')

		mars_temp = mars_soup.find('ol', class_='stream-items')
		mars_weather = mars_temp.find('p', class_='tweet-text').text
		print(f'Mars Weather: {mars_weather}')

		mars['mars_weather'] = mars_weather

		return mars

	finally:
		browser.quit()

def scrape_facts():
	facts_url = 'https://space-facts.com/mars/'
	browser.visit(facts_url)
	facts_html = browser.html
	facts_soup = BeautifulSoup(facts_html, 'html.parser')

	tables = pd.read_html(facts_url)
	fact_df = tables[0]
	fact_df_html = fact_df.to_html()

	mars['tables'] = fact_df_html

	return mars

def scrape_hemi():
	try:
		browser = init_browser
		hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
		browser.visit(hemispheres_url)
		hemi_html = browser.html
		hemi_soup = BeautifulSoup(hemi_html, 'html.parser')      

		spheres = []
		for x in range (4): 
		    images = browser.find_by_tag('h3')
		    images[x].click()
		    hemi_html = browser.html
		    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
		    bit = hemi_soup.find('img', class_='wide-image')['src']
		    sphere_title = hemi_soup.find('h2', class_='title').text
		    sphere_url = (f'https://astrogeology.usgs.gov{bit}')
		    dict_hemi = {'Title' : sphere_title, 'url': sphere_url}
		    spheres.append(dict_hemi)

	    mars['spheres'] = spheres

		return mars

	finally: 
		browser.quit()