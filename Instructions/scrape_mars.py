from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt




def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    
mars_data = {}


# NASA Mars News
def scrape_mars_news():
    browser = init_browser()
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(nasa_url)

    html = browser.html
    # create a soup object from the html
    img_soup = BeautifulSoup(html, "html.parser")
    result = img_soup.find_all('div', class_="slide")
    news_title = result.find('div', class_="content_title").find('a').get_text()
    news_p = result.find('div', class_ = 'rollover_description').find('div', class_ = "rollover_description_inner").get_text()
    # add our title and paragraph to mars data 
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p
    browser.quit()
    return mars_data

#JPL Mars Space Images   
def scrape_jpl(): 
    browser = init_browser()
    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    browser.find_by_id("full_image").click()
    browser.click_link_by_partial_text("more info")

    # create soup object from html
    html = browser.html
    jpl_soup = BeautifulSoup(html, "html.parser")
    img = jpl_soup.find('img', class_ = "main_image")["src"]
    featured_image_url = 'https://www.jpl.nasa.gov' + img
 
    mars_data["featured_image_url"] = featured_image_url

    browser.quit()
    return mars_data


# Mars Weather
def scrape_mars_weather():
    browser = init_browser()
    mars_weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)

    # create soup object from html
    html = browser.html
    mars_weather_soup = BeautifulSoup(html, "html.parser")
    mars_weather_results = mars_weather_soup.find_all('div', class_="js-tweet-text-container")
    for result in mars_weather_results: 
        mars_weather = result.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
        if 'Sol' and 'pressure'in mars_weather:     
            # print(mars_weather)
            break
        else: 
            pass

    mars_data["mars_weather"] = mars_weather

    browser.quit()
    return mars_data


#Mars Facts
def scrape_mars_facts():
    # Mars Weather
    browser = init_browser()
    mars_fact_url = 'https://space-facts.com/mars/'
    browser.visit(mars_fact_url)

    # create soup object from html
    tables = pd.read_html(mars_fact_url)
    df_mars = tables[0]
    df_mars.columns = ["Facts","Values"]
    df_mars = df_mars.set_index("Facts")
    mars_facts = df_mars.to_html(index = True, header =True)
    mars_facts.replace('\n ','')
    mars_data["mars_facts"] = mars_facts

    browser.quit()
    return mars_data

def scrape_mars_hemispheres():
    browser = init_browser()
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url) 
    html = browser.html
    mars_hemispheres_soup = BeautifulSoup(html,'html.parser')
    hemispheres = mars_hemispheres_soup.find_all("div", class_="item")
    hem_dic =[]
    for h in hemispheres:
        title = h.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = h.find("a")["href"]
        img_link = 'https://astrogeology.usgs.gov' + end_link
        browser.visit(img_link)
        html = browser.html
        mars_hemispheres_soup=BeautifulSoup(html, "html.parser")
        img_store = mars_hemispheres_soup.find("div", class_="downloads")
        imag_url = img_store.find("a")["href"]
        hem_dic.append({"title": title, "img_url": imag_url})
        mars_data["hem_dic"] = hem_dic

    browser.quit()
    return mars_data


def getData(mars_data):
    final_report = ""
    for fp in mars_data:
        final_report += " " + fp.get_text()
        print(final_report)

    return final_report



    