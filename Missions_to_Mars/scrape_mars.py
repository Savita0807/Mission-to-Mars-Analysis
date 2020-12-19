from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd 


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news title and News para
    results_title = soup.find_all('div', class_="list_text")
    Title_text=[]
    Para_text=[]

    for result in results_title:
        title = result.find('div', class_='content_title')
        Title_text.append(title.a.text)
    
        try:
  
            Para = result.find('div', class_='article_teaser_body')
            para = Para.text.lstrip()
            Para_text.append(para)
    
            news_title = Title_text[0]
            news_p = Para_text[0]
                    
        except AttributeError as e:
            print(e)   
        
# print(news_title)
# print(news_p)    

    # Get the Featured Image url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Featured Image url
    results_img = soup.find('article')['style']
    featured_image_url = results_img.replace("background-image: url('", "https://www.jpl.nasa.gov")
    featured_image_url = featured_image_url.replace("');","")

    # Mars Facts url
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    Mars_df = tables[0]
    Mars_df.columns = ['', 'Mars']
    Mars_df.set_index('', inplace=True)
    Mars_html_table = Mars_df.to_html(classes="table table-striped table-responsive")

    # Mars Hemispheres
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)  
    # Retrieve page with the requests module and parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')
    results_hemi = soup.find_all('div', class_="item")
    hemisphere_image_urls=[]
    for result in results_hemi:
        Item_url = result.a['href']
        img_title = result.h3.text
    
        Final_url = 'https://astrogeology.usgs.gov/'+Item_url
        url= Final_url
        browser.visit(url)
    
        html = browser.html
        soup = bs(html, 'html.parser')
    
        find_url= soup.find('img', class_="wide-image")['src']
    
        img_url = 'https://astrogeology.usgs.gov/'+find_url
    
        hemi_url={"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(hemi_url)
    
    # Store data in a dictionary
    Mars_data = {
        "News_Title": news_title,
        "News_Para": news_p,
        "Img_url": featured_image_url,
        "Facts_tbl":  Mars_html_table,
        "Img_hemi": hemisphere_image_urls
    }


    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return Mars_data

# Mars_data = scrape_info()    
# print(Mars_data)
