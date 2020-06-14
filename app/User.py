from .gimage import start_scrapper,get_image_link


class User:
    def __init__(self):
        #browser object per user
        self.browser = None
        #generator object for getting the image link
        self.next_link = None
    def start_browser(self):
        self.browser = start_scrapper()
        self.next_link = get_image_link()
    
    def close_browser(self):
        self.browser.close()
        