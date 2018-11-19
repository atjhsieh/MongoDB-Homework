
# coding: utf-8

# In[1]:


# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import shutil
import pandas as pd


# In[2]:


# URL of page to be scraped
url = "https://mars.nasa.gov/news/"


# In[3]:


# Retrieve page with the requests module
response = requests.get(url)


# In[4]:


# Create BeautifulSoup object; parse with "html.parser"
soup = bs(response.text, "html.parser")


# In[5]:


#print(soup.prettify())


# In[6]:


# results are returned as an iterable list
results_title = soup.find_all('div', class_="content_title")
results_p = soup.find_all('div', class_="rollover_description_inner")


# In[7]:


news_title = results_title[0].find('a').text.strip()
news_p = results_p[0].text.strip()
#print(news_title)
#print(news_p)


# In[8]:


img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"


# In[9]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(img)


# In[10]:


html = browser.html
soup = bs(html, 'html.parser')


# In[11]:


#print(soup.prettify())


# In[12]:


imageurl = soup.find_all('div', class_="carousel_items")
#imageurl


# In[13]:


for i in imageurl:
    featured_image_url = i.article["style"]
featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url.split("('")[1].split("');")[0]
#featured_image_url


# In[14]:


response = requests.get(featured_image_url)
if response.status_code == 200:
    with open("FeaturedImage.jpg", 'wb') as f:
        f.write(response.content)


# In[15]:


twt = "https://twitter.com/marswxreport?lang=en"


# In[16]:


response = requests.get(twt)
soup = bs(response.text, "html.parser")


# In[17]:


#print(soup.prettify())


# In[18]:


results_weather = soup.find_all('div', class_="js-tweet-text-container")
mars_weather = results_weather[0].p.text.strip()
#mars_weather


# In[19]:


fct = "http://space-facts.com/mars/"
facts = pd.read_html(fct)
df = facts[0]
#df


# In[20]:


df.columns = ["Statistics","Values"]
#df.head()


# In[21]:


df.set_index('Statistics', inplace=True)
#df.head()


# In[22]:


html_table = df.to_html()
html_table.replace('\n', '')
#html_table


# In[23]:


hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
]


# In[24]:


mars_data =    [
        {"news title":news_title,"news description":news_p,
         "image":featured_image_url,"weather":mars_weather,
         "facts":html_table, "hemisphere image":hemisphere_image_urls}
    ]


# In[25]:


def scrape():
    return mars_data


# In[26]:


#mars_data

