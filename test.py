#interact with website like person?
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

#get data from page?
from bs4 import BeautifulSoup
import requests

cService = webdriver.ChromeService(executable_path='Users/roseromo/Downloads/chromedriver-mac-x64')

driver = webdriver.Chrome(service=cService)

""" url = 'https://www.ulta.com/'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html')

print(soup) """

driver.get('https://hoopshype.com/salaries/players/')
