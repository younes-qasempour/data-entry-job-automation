from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time


def clean_price(price_str):
    # Remove commas, '+', '/mo', and '1 bd' or '1bd'
    cleaned = price_str.replace(',', '').replace('+', '').replace('/mo', '').replace(' 1 bd', '').replace(' 1bd', '')
    # Return only the dollar sign and digits
    return f"${cleaned[1:]}"


class DataEntryJob:

    def __init__(self):
        self.zillow_webpage = requests.get("https://appbrewery.github.io/Zillow-Clone/").content
        self.soup = BeautifulSoup(self.zillow_webpage, 'html.parser')
        self.driver = webdriver.Chrome()

        self.links = []
        self.prices = []
        self.addresses = []

    def get_data(self):
        each_article = self.soup.find_all("article")
        for article in each_article:
            self.links.append(article.find("a").get("href"))
            self.prices.append(clean_price(article.css.select(".PropertyCardWrapper__StyledPriceLine")[0].text))
            self.addresses.append(article.find("address").text.strip())

    def fill_form(self):
        for item in range(len(self.links)):
            form_link = (
                "https://docs.google.com/forms/d/e/1FAIpQLSfQ4xoX6iEQNl2Ap"
                "9h8OyV_HGdjzV7x442tQpIiprwFE9793g/viewform?usp=header")
            self.driver.get(form_link)
            time.sleep(5)
            address_entry = self.driver.find_element(By.XPATH, "(//input[@type='text'])[1]")
            price_entry = self.driver.find_element(By.XPATH, "(//input[@type='text'])[2]")
            link_entry = self.driver.find_element(By.XPATH, "(//input[@type='text'])[3]")
            address_entry.send_keys(self.addresses[item])
            price_entry.send_keys(self.prices[item])
            link_entry.send_keys(self.links[item])
            time.sleep(1)
            self.driver.find_element(By.XPATH, "(//span[@class='l4V7wb Fxmcue'])[1]").click()


bot = DataEntryJob()
bot.get_data()
bot.fill_form()
