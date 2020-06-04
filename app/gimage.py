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

#global browser variable
browser = None
total_images = 40


driver_path  = os.path.dirname(__file__)
driver_path = os.path.join(driver_path,'chromedriver.exe')

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
    limit = len(images_div)
    print(f'\n\nthere are {limit} in here\n\n')
    i = 0
    while i<limit:
        yield images_div[i]
        i=i+1
    return None


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
    
    while i < total_images:
        image_div = next(all_image_divs)
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
    #command_executor = 'http://127.0.0.1:49670'
    #session_id = 'b6c04d8f371ddbae7d39c62a8bba4ac8'
    #opening remote browser persistent
    #browser = open_remote_browser(command_executor,session_id)
    global browser
    chrome_option = webdriver.ChromeOptions()
    #chrome_option.add_argument('incognito')
    chrome_option.add_argument("headless")
    #options = webdriver.FirefoxOptions()
    #options.add_argument('headless')
    
    browser = webdriver.Chrome(chrome_options=chrome_option,executable_path=driver_path)#(chrome_options=chrome_option)#direct_chrome_browser()
    #search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    #calling  get_image_link with image divs