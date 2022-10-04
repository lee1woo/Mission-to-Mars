
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt



def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    print ("\n******************\n")
    
    print (executable_path)
    print ("\n******************\n")
    browser = Browser('chrome', **executable_path, headless=True)
    print ("\n******************\n")
    
    print (browser)
    print ("\n******************\n")

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')

    # slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    # news_title

    # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    # news_p

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):

# # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

# Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

# # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel
    
    except AttributeError:
        return None

# Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    try:

        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    results = hemi_soup.find_all('div', class_ = 'description')
    for result in results:
        title = result.find('h3').text
        browser.links.find_by_partial_text(title).click()

        html = browser.html
        hemi_soup = soup(html, 'html.parser')
        href = hemi_soup.find('a', text = 'Sample')['href']
        hemisphere_image_urls.append(
            {'img_url': url + href,
            'title': title})
        browser.back()

    return hemisphere_image_urls
        
if __name__ == "__main__":

    print(scrape_all())

# df = pd.read_html('https://galaxyfacts-mars.com')[0]
# df.columns=['description', 'Mars', 'Earth']
# df.set_index('description', inplace=True)
# df

# df.to_html()


# browser.quit()
