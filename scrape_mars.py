# import dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import time
from pandas import pandas as pd
import os

# Start Chrome Driver to navigate through websites
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Main dictionary to store scraped data
mars_data = {}

def scrape_info():
    # -----
    # Scrape for News Titles and Paragraph Text
    news_url = "https://mars.nasa.gov/news/"

    browser = init_browser()
    browser.visit(news_url)

    time.sleep(1) # Set time sleep to 1 sec. Increase time if needs longer to scrape

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Collect the latest News Title and Paragraph Text
    news_title = soup.find('div', class_ = 'content_title').text
    news_p = soup.find('div', class_ = 'article_teaser_body').text

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p
    }

    # Close the browser after scraping
    browser.quit()
    print(mars_data)

    # -----
    # JPL Mars Space Images - Featured Image
    jpl_home = "https://www.jpl.nasa.gov"
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # visit browser must remain outside of browser quit or will create endless loop
    browser = init_browser()
    browser.visit(jpl_url)
    time.sleep(1)

    try:
        for url in jpl_url:
            
            # click on first button
            browser.click_link_by_partial_text('FULL IMAGE')
            time.sleep(2)
            
            # click on next page button
            browser.click_link_by_partial_text('more info')
            time.sleep(1)
            
            # Scrape page into Soup
            html = browser.html
            soup = bs(html, "html.parser")
            
            #  Find image and save into variable
            figure_img = soup.find('figure', class_="lede").find('a')['href']

            # Create url of image
            feature_img_url = jpl_home + figure_img
            
            # print(f"Feature image url: {feature_img_url}")

    except ElementDoesNotExist:
        print("Scraping Complete")
        
    # Close the browser after scraping
    browser.quit()

    # updating dictionary must be outside of loop
    mars_data["feature_img_url"] = feature_img_url
    print(mars_data)

    #-----
    # Mars weather
    mars_twitter = "https://twitter.com/marswxreport?lang=en"

    # visit browser must remain outside of browser quit or will create endless loop
    browser = init_browser()
    browser.visit(mars_twitter)
    time.sleep(1)

    try:
        for url in mars_twitter:
            # Scrape page into Soup
            html = browser.html
            soup = bs(html, "html.parser")

            # Collect the latest tweet
            mars_weather = (soup.find('p', class_ = 'tweet-text').text)
        
    except ElementDoesNotExist:
        print("Scraping Complete")
        
    # Close the browser after scraping
    browser.quit()

    # Store data in a dictionary
    mars_data["mars_weather"] = mars_weather
    print(mars_data)

    # -----
    # Mars facts table
    mars_facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(mars_facts_url, header=None)
    df = tables[0]
    df.columns = ["Key", "Measurement"]
    df.to_html('tables/mars_table.html', index = False)

    # find current path
    file_path = os.getcwd()
    table_path = file_path[0] + "tables/mars_table.html"
    mars_data["table_path"] = table_path
    print(mars_data)

    # -----
    # Mars Hemispheres
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser = init_browser()
    browser.visit(hemi_url)
    time.sleep(1)

    # Gather list of names to scrape for
    hemi_names = []
    for n in range(4):
        name = browser.find_by_css('h3')[n].text
        hemi_names.append(name)
    print(hemi_names)

    mars_img = []

    try:
        for name in hemi_names:
            browser.click_link_by_partial_text(name)
            time.sleep(1)

            html = browser.html
            soup = bs(html, "html.parser")

            img_url = soup.find('div', class_ ='downloads').find('li').find('a')['href']
            print(f"Scraping {name}")

            if any(x.get("img_title") == name for x in mars_img):
                print("No new items added.")
            else:
                # Append dictionaries to a list
                mars_img.append({
                    "img_title": name,
                    "img_url": img_url})
                
            browser.back()
            
    except ElementDoesNotExist:
        print("Scraping Complete")
        
    browser.quit()

    # save urls to main mars_data
    mars_data["Mars images"] = mars_img

    return mars_data

print("You made it to Mars!")
print(mars_data)