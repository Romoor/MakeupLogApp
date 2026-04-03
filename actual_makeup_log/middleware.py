from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
class SeleniumMiddleWare(object):

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        content = self.driver.page_source
        return HtmlResponse(request.url, encoding='utf-8',
                        body=content, request=request)

    def process_response(self, request, response, spider):
        return response
        
    def spider_closed(self, spider):
        self.driver.quit()