import os
import re
import requests
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
                "birth_date": 1962,
            },
            "Natalie Portman": {
                "url": "https://www.imdb.com/fr/name/nm0000204/",
                "birth_date": 1981,
            }
        }

    def scrape(self):
        data = np.array([])
        cookies_declined = False  # Init
        for actor in self.actors:
            self.driver.get(self.actors[actor]["url"])

            if not cookies_declined:
                decline_button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='reject-button']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", decline_button)
                decline_button.click()
                cookies_declined = True

            photos_button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a.ipc-btn--on-onBase:nth-child(2)")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", photos_button)
            self.driver.execute_script("arguments[0].click();", photos_button)  # JS click due to element superposition

            if os.path.exists(f"../Datasets/IMDB Scrap/{actor}") is False:  # Create folder if it doesn't exist
                os.makedirs(f"../Datasets/IMDB Scrap/{actor}")

            i = 1  # Init
            gallery_count_element = WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="action-bar__gallery-count"]'))            )
            nb_total_images = int(gallery_count_element.text.replace(f"{i} de ", "").replace(" ", "").strip())
            while i <= nb_total_images:
                og_image = self.driver.find_element(By.XPATH, "//meta[@property='og:image']")
                image_url = og_image.get_attribute("content")
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    image_path = f"../Datasets/IMDB Scrap/{actor}/{i}.jpg"
                    with open(image_path, 'wb') as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    og_description = self.driver.find_element(By.XPATH, "//meta[@property='og:description']")
                    og_description = og_description.get_attribute("content")
                    match = re.search(r'(?:in|at an event for) (.+) \((\d{4})\)', og_description)
                    if match:
                        title = match.group(1)
                        age = int(match.group(2)) - int(self.actors[actor]["birth_date"])
                        np.append(data, [actor, i, title, age])
                        print(f"{actor} ({(i/nb_total_images)*100:.2f}%) - Image and metadata {i}/{nb_total_images} saved")
                    else:
                        os.remove(image_path)
                        print(f"{actor} ({(i/nb_total_images)*100:.2f}%) - Failed to gather metadata for image {i}/{nb_total_images}")
                else:
                    print(f"{actor} ({(i/nb_total_images)*100:.2f}%) - Failed to download image {i}/{nb_total_images}")

                i += 1
                next_button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.sc-c7067688-2')))
                ActionChains(self.driver).move_by_offset(15, 15).perform()  # Move mouse to avoid button diseapearing
                ActionChains(self.driver).move_to_element(next_button).perform()           # Move mouse to avoid button diseapearing
                self.driver.execute_script("arguments[0].click();", next_button)

        np.savetxt("../Datasets/IMDB Scrap/imdb_scrap.csv", data, delimiter=",", fmt="%s", header="Actor,Title,Age")
        print("Scraping done!")

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    scraper = ImdbScrape()
    scraper.scrape()
    scraper.close()