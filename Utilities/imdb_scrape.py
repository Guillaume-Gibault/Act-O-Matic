import os
import requests
from selenium import webdriver
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
        cookies_declined = False  # Init
        for actor in self.actors:
            i = 1  # Init
            self.driver.get(self.actors[actor]["url"])
            if not cookies_declined:
                decline_button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='reject-button']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", decline_button)
                decline_button.click()
                cookies_declined = True
            photos_button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a.ipc-btn--on-onBase:nth-child(2)")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", photos_button)
            self.driver.execute_script("arguments[0].click();", photos_button)
            if os.path.exists(f"../Datasets/IMDB Scrap/{actor}") is False:  # Create folder if it doesn't exist
                os.makedirs(f"../Datasets/IMDB Scrap/{actor}")
            image_element = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'div.sc-7c0a9e7c-3 img')))
            image_url = image_element.get_attribute("src")
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image_path = os.path.join(os.getcwd(), f"../Datasets/IMDB Scrap/{actor}/{i}.jpg")
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Image enregistrée sous : {image_path}")
                i += 1
            else:
                print("Échec du téléchargement de l'image.")

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    scraper = ImdbScrape()
    scraper.scrape()
    scraper.close()