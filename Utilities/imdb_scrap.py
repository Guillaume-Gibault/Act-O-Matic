import os
import re
import requests
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from concurrent.futures import ThreadPoolExecutor


class ImdbScrape:
    def __init__(self):
        self.actors = {
            "Tom Cruise": {
                "url": "https://www.imdb.com/fr/name/nm0000129/",
                "birth_date": 1962,
            },
            "Natalie Portman": {
                "url": "https://www.imdb.com/fr/name/nm0000204/",
                "birth_date": 1981,
            },
            "Will Smith Crop": {
                "url": "https://www.imdb.com/fr/name/nm0000226/",
                "birth_date": 1968,
            },
            "Brad Pitt": {
                "url": "https://www.imdb.com/fr/name/nm0000093/",
                "birth_date": 1963,
            },
        }

    def scrape_actor(self, actor, actor_data):
        driver = webdriver.Firefox()
        driver.maximize_window()
        wait = WebDriverWait(driver, 30)
        output = np.array(["Actor", "Image", "Title", "Age"])
        cookies_declined = False

        try:
            driver.get(actor_data["url"])

            if not cookies_declined:
                decline_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='reject-button']")))
                driver.execute_script("arguments[0].scrollIntoView(true);", decline_button)
                decline_button.click()
                cookies_declined = True

            photos_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a.ipc-btn--on-onBase:nth-child(2)")))
            driver.execute_script("arguments[0].scrollIntoView(true);", photos_button)
            driver.execute_script("arguments[0].click();", photos_button)

            actor_folder = f"../Datasets/IMDB Scrap/{actor}"
            if not os.path.exists(actor_folder):
                os.makedirs(actor_folder)

            i = 1
            gallery_count_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="action-bar__gallery-count"]')))
            nb_total_images = int(gallery_count_element.text.replace(f"{i} de ", "").replace(" ", "").strip())

            while i <= nb_total_images:
                og_image = driver.find_element(By.XPATH, "//meta[@property='og:image']")
                image_url = og_image.get_attribute("content")
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    image_path = f"{actor_folder}/{i}.jpg"
                    with open(image_path, 'wb') as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    og_description = driver.find_element(By.XPATH, "//meta[@property='og:description']")
                    og_description = og_description.get_attribute("content")
                    match = re.search(r'(?:in|at an event for) (.+) \((\d{4})\)', og_description)
                    if match:
                        title = match.group(1)
                        age = int(match.group(2)) - int(actor_data["birth_date"])
                        output = np.vstack([output, [actor, i, title, age]])
                        np.savetxt(f"{actor_folder}/Index.csv", output, fmt="%s", delimiter=";")
                        print(f"{actor} ({(i/nb_total_images)*100:.2f}%) - Image and metadata {i}/{nb_total_images} saved")
                    else:
                        os.remove(image_path)
                        print(f"{actor} ({(i/nb_total_images)*100:.2f}%) - Failed to gather metadata for image {i}/{nb_total_images}")
                else:
                    print(f"{actor} ({(i/nb_total_images)*100:.2f}%) - Failed to download image {i}/{nb_total_images}")

                i += 1
                next_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.sc-c7067688-2')))
                ActionChains(driver).move_by_offset(15, 15).perform()
                ActionChains(driver).move_to_element(next_button).perform()
                driver.execute_script("arguments[0].click();", next_button)

        except Exception as e:
            print(f"Error while scraping {actor}: {e}")
        finally:
            driver.quit()

    def scrape_all(self):
        with ThreadPoolExecutor(max_workers=4) as executor:  # Limit to 2 threads to avoid overwhelming system resources
            futures = [executor.submit(self.scrape_actor, actor, data) for actor, data in self.actors.items()]
            for future in futures:
                future.result()  # Wait for all threads to complete


if __name__ == "__main__":
    scraper = ImdbScrape()
    scraper.scrape_all()
    print("Scraping completed.")
