from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import requests
import shutil
import json
from flask import session

class user:
    def __init__(self):
        print('object created')
        self.browser = webdriver.Chrome()

    def prints(self):
        print(self.browser)


if __name__ == "__main__":
    u=user()
    print(u.__dict__)
    session['user'] = user().__dict__
    print(json.dumps(u.__dict__))


'''
executor_url = browser.command_executor._url
session_id = browser.session_id

print(executor_url)
print(session_id)

search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
q="horizon zero dawn"

search_url=f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
browser.get(search_url)
'''