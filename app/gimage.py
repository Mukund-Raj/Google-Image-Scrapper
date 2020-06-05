from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import shutil
import os
import json
from app import ENV

#global variables start

#global browser variable
browser = None
total_images = 100

#global variables end
'''
total number of images discovered till now
so that we can keep track as user wants more images and clicking
load more again and again and to start the get_all_the_image_divs
generator so that we don't get repeated images over and over
'''
exhaustion = 0

#a indicator of total images get in one find_elements_by_css_selector
one_time_limit = 0

def WAIT(how_much=1):
    ''' Default value is 1 @param how_much '''
    time.sleep(how_much)

def direct_chrome_browser():
    #chrome_option = webdriver.ChromeOptions()
    #chrome_option.add_argument("headless")
    #chrome_option.binary_location = r'C:\Users\RAJ\AppData\Local\Google\Chrome SxS\Application\chrome.exe'
    browser = webdriver.Chrome()#(chrome_options=chrome_option)
    return browser

#active even after close function
def open_remote_browser(command_executor_arg,sess_id):
    browser = webdriver.Remote(command_executor_arg,desired_capabilities={})
    browser.session_id = sess_id
    return browser

#get all th image links not the actual big size image
def get_all_the_image_divs():
    images_div = browser.find_elements_by_css_selector('img.rg_i')
    one_time_limit = len(images_div)
    print(f'\n\nthere are {one_time_limit} in here\n\n')
    i = exhaustion
    while i<one_time_limit:
        yield images_div[i]
        i=i+1
    yield None


def get_actual_link(image_div):
    image_link = browser.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')
    #WAIT()
    src = image_link
    #print("in function ",src)
    #print(src.get_attribute('src'))
    #print(type(src.get_attribute('src')))
    #only return src only starting from http[s]
    if 'https' in src.get_attribute('src') or 'htpps' in src.get_attribute('src'):
        #print(src.get_attribute('src'))
        return src
    
    return None

def get_image_size():
    #WAIT(1)
    images_size_element = browser.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/span')
    #print(images_size_element.get_attribute('innerHTML'))
    return images_size_element

#get actual link of the image it is a generator
def get_image_link():
    #wait 1 sec to load the page
    WAIT(1)  
    i=0
    count = 0

    total_links={}
    total_links["links"] = []

    #calling get_all_the_image_divs() and limiting the number of links    
    all_image_divs = get_all_the_image_divs()
    #print(len(all_image_divs))
    
    #yield 5 image link at a time
    max =  5
    j = 0
    src = None
    
    #while i < total_images:
    while True:
        image_div = next(all_image_divs)
        if image_div is None:
            all_image_divs = get_all_the_image_divs()
            image_div = next(all_image_divs)
            global exhaustion
            exhaustion = exhaustion + one_time_limit

        image_div.click()
        WAIT(1)
        single_link={}

        #then get the link of actual image
        src = get_actual_link(image_div)
        #for getting the size of image as in the span tag
        try:
            if src is None:
                #print('src is none')
                raise OSError()

            single_link['link'] = src.get_attribute('src')
            #WAIT(1)
            try:
                image_size = get_image_size()
            except:
                i = i+1
                continue
                print("error in span text")

            image_size = str(image_size.get_attribute('innerHTML')).split(' ')
            single_link['width'] = image_size[0]
            single_link['height'] = image_size[-1]
            #total_links['links'].append(single_link)
            j = j + 1
            print("got one link")
            WAIT(1)
            count = count + 1 
        except:
            i=i+1
            continue    
            print('no src')
        
        i=i+1
        
        #if j < max:
        yield single_link
        
        #reinitialize total links so that we do not get repeated values
        #total_links["links"] = []
        #j = 0
    browser.close()
    print('got ',count,' links')

def search_query(query):
    search_url=f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img"
    browser.get(search_url)
    #get_image_link()

def start_scrapper():
    '''
    instantiate chrome browser
    '''
    #command_executor = 'http://127.0.0.1:49670'
    #session_id = 'b6c04d8f371ddbae7d39c62a8bba4ac8'
    #opening remote browser persistent
    #browser = open_remote_browser(command_executor,session_id)
    #chrome_option.add_argument('incognito')
    #options = webdriver.FirefoxOptions()
    #options.add_argument('headless')
    
    global browser
    #chrome options for deploying on heroku
    chrome_option = webdriver.ChromeOptions()
    if  ENV == 'dev':
        print('in dev')
        driver_path  = os.path.dirname(__file__)
        driver_path = os.path.join(driver_path,'chromedriver.exe')
        chrome_option.add_argument("--headless")
        chrome_option.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(chrome_options=chrome_option,executable_path=driver_path)

    elif ENV == 'prod':
        chrome_option.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
        chrome_option.add_argument("--headless")
        chrome_option.add_argument("--disable-dev-shm-usage")
        chrome_option.add_argument("--no-sandbox")
        browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_option)