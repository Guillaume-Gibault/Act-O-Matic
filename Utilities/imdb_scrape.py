import os
import time
import pyperclip
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class ImdbScrape:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30)
        self.actors = {
            "Tom Cruise": {
                "url": "https://www.imdb.com/fr/name/nm0000129/",
                "birth_date": "1962",
            },
            "Natalie Portman": {
                "url": "https://www.imdb.com/fr/name/nm0000204/",
                "birth_date": "1981",
            }
        }

    def scrape(self):
        cookies_declined = False
        for actor in self.actors:
            self.driver.get(self.actors[actor]["url"])
            if not cookies_declined:
                decline_button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='reject-button']")))
                decline_button.click()
                cookies_declined = True
            photos_button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a.ipc-btn--on-onBase:nth-child(2)")))
            photos_button.click()

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    scraper = ImdbScrape()
    scraper.scrape()
    scraper.close()