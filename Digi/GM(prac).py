# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class ScrapeRestaurant:
#     def __init__(self):
#         # Use Firefox driver without specifying the path
#         firefox_options = webdriver.FirefoxOptions()
#         firefox_options.set_preference("dom.webnotifications.enabled", False)
#         self.driver = webdriver.Firefox(options=firefox_options)
#         self.url = "https://www.google.com/maps/search/food+vendor+miami+usa/@25.7825389,-80.3118612,12z/data=!3m1!4b1?entry=ttu"

#     def scrape(self):
#         try:
#             # Open the link
#             self.driver.get(self.url)

#             # Wait for the top list page element to be present
#             top_list_page = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "div.section-result")))

#             # Use JavaScript to click on the top list page
#             self.driver.execute_script("arguments[0].click();", top_list_page)

#             # Wait for the side bar to be present
#             side_bar = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "div.section-layout.section-scrollbox")))

#             # Wait for the restaurant name to be present
#             restaurant_name = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "h1 span"))).text

#             # Wait for the reviews count to be visible
#             reviews_count = WebDriverWait(self.driver, 10).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, "div.gm2-caption div span"))).text

#             print("Restaurant Name:", restaurant_name)
#             print("Reviews Count:", reviews_count)

#         except Exception as e:
#             print("Error:", e)

#         finally:
#             self.driver.quit()

# # Create an instance of the class and call the scrape method
# scraper = ScrapeRestaurant()
# scraper.scrape()

# Project One : 

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 

options = Options()
options.add_experimental_option("detach", True)

path = r"D:/Chrome Driver/chromedriver-win64/chromedriver.exe"

service = Service(path)

driver = webdriver.Chrome(path, options=options, service=service)
driver.get("https://www.google.com/maps/search/food+vendor+miami+usa/@25.7825389,-80.3118612,12z/data=!3m1!4b1?entry=ttu")

driver.maximize_window()
time.sleep(3)

search = driver.find_element(By.NAME, "q")
search.clear()
search.send_keys("dentist new york")
search.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 10)
dentists = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Nv2PK")))

names = []
locations = []
ranks = []
websites = []

for dentist in dentists:
  try:
    dentist.click()

    dentist_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lfPIob")))
    print(f"- Dentist Name: {dentist_name.text}")
    names.append(dentist_name.text)
    time.sleep(3)

    location_entry = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "RcCsl")))
    dentist_location = location_entry.find_element(By.CLASS_NAME, "rogA2c")
    print(f"- Dentist Location: {dentist_location.text}")
    locations.append(dentist_location.text)
    time.sleep(3)

    dentist_rank = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "F7nice")))
    print(f"- Dentist Rank: {dentist_rank.text}")
    ranks.append(dentist_rank.text)
    time.sleep(3)

    dentist_website = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ITvuef ")))
    print(f"- Dentist WebSite: {dentist_website.text}")
    websites.append(dentist_website.text)
    time.sleep(3)

    print("-" * 20)
    print()
    time.sleep(5)

  except Exception:
    continue

  finally:
    driver.back()

excel_file_path= r"D:\projects\dentists_info.xlsx"

# Create a DataFrame from the lists
data = {'Dentist Name': names, 'Location': locations, 'Rank': ranks, 'Website': websites}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel(excel_file_path, index=False)
print(f'Data has been saved to {excel_file_path}')

# aIFcqe
# LoJzbe keynav-mode-off screen-mode