# Import Dependencies
from bs4 import BeautifulSoup
import requests
import os
import pymongo
from splinter import Browser
import pandas as pd

def init_browser():
     executable_path = {'executable_path': 'chromedriver.exe'}
     return Browser('chrome', **executable_path, headless=False)

mars_data = {}

# NASA Mars News
def scrape_mars_news():
    browser = init_browser()

    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)
    html = browser.html
    soup = BeautifulSoup(html, "lxml")

    result = soup.find("div", class_='list_text')
    news_title = result.find("div", class_="content_title").text
    news_p = result.find("div", class_ ="article_teaser_body").text

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p

    return mars_data

    browser.quit()

# JPL Featured Image
def scrape_mars_image():
    browser = init_browser()

    jpl_image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_image_url)
    html_image = browser.html
    soup_image = BeautifulSoup(html_image, "lxml")

    image = soup_image.find("article")['style'][23:-3]
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + image
    
    mars_data['featured_image_url'] = featured_image_url

    return mars_data

    browser.quit()

# Mars Weather

def scrape_mars_weather():
    browser = init_browser()    

    weather_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html_mars_temp = browser.html
    bs = BeautifulSoup(html_mars_temp, "html.parser")
    mars_weather = bs.select("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[7].get_text(strip=True)[8:-26]

    mars_data['mars_weather'] = mars_weather

    return mars_data

    browser.quit()

# Mars Facts

def scrape_mars_facts():
    url_mars_facts = "https://space-facts.com/mars/"
    tables = pd.read_html(url_mars_facts)
    df=tables[1]
    df.columns=['Description', 'Mars Values']
    df.set_index('Description', inplace=True)
    data = df.to_html()

    mars_data['mars_facts'] = data

    return mars_data

# Mars Hemispheres

def scrape_mars_hemispheres():
    browser = init_browser()

    url_hemisphere="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)
    html_mars_hemi = browser.html
    bs_hemi = BeautifulSoup(html_mars_hemi, "html.parser")

    items = bs_hemi.find_all('div', class_="item")

    hemisphere_image_urls = []

    base_url = 'https://astrogeology.usgs.gov'

    for item in items:
        title = item.find('h3').text
        url_path = item.find('a', class_="itemLink product-item")['href']
        browser.visit(base_url + url_path)
        html_full_image = browser.html
        soup2=BeautifulSoup(html_full_image, "html.parser")
        img_url = base_url + soup2.find('img',class_='wide-image')['src']
        hemisphere_image_urls.append({'title':title, 'img_url':img_url})

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data

    browser.quit()