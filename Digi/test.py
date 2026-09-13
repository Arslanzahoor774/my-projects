#FIRST WAY
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from random import randint

class ScrapearGMaps:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def click_first_five_restaurants(self):
        collected_data = []
        for i in range(5):
            try:
                # Assuming 'm6QErb DxyBCb kA9KIf dS8AEf ecceSd' is the class for restaurant listings
                restaurants = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")))
                restaurants[i].click()
                time.sleep(randint(2, 4))

                # Scrape data
                name = self.get_name()
                address = self.get_address()
                time_table = self.get_timetable()
                collected_data.append({'name': name, 'address': address, 'timetable': time_table})

                # Go back to the list
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[jsaction*='pane.back']"))).click()
                time.sleep(randint(2, 4))

            except Exception as e:
                print(f"Error in clicking restaurant {i + 1}: {e}")
                break

        return collected_data

    def get_name(self):
        try:
            # Assuming 'h1.header-title span' is the class for the name
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.header-title span"))).text
        except Exception:
            return "Name not found"

    def get_address(self):
        try:
            # Assuming 'button[data-item-id='address'] div' is the class for the address
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-item-id='address'] div"))).text
        except Exception:
            return "Address not found"

    def click_open_close_time(self):
        try:
            # Assuming the class for the hours button
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[jsaction*='hours.expand']")))
            button.click()
        except Exception:
            print("Error clicking open/close time")

    def get_timetable(self):
        try:
            df_result = pd.DataFrame(columns=['day', 'open_time'])
            # Assuming these are the classes for week days and open times
            week_days = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "th[class*='weekday'] > div")))

            open_time = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td[class*='hours'] > ul > li")))

            if len(week_days) >= 7 and len(open_time) >= 7:
                for i in range(7):
                    day = week_days[i].get_attribute('innerHTML')
                    time = open_time[i].get_attribute('innerHTML')
                    df_result = df_result.append({'day': day, 'open_time': time}, ignore_index=True)

            return df_result
        except Exception:
            return pd.DataFrame(columns=['day', 'open_time'])

    def scrape(self, query):
        try:
            query = query.replace(" ", "+")
            url = f"https://www.google.com/maps/search/{query}"
            self.driver.get(url)
            time.sleep(randint(2, 4))

            return self.click_first_five_restaurants()

        except Exception as e:
            print(f"Error in scrape method: {e}")
            return []

        finally:
            self.driver.quit()
            print("Data extraction completed.")

# Usage of the class
query = "food vendor miami usa"
gmaps = ScrapearGMaps()
data = gmaps.scrape(query)

# Convert to DataFrame and save to CSV
if data:
    df = pd.DataFrame(data)
    df.to_csv(f"{query}_data.csv", index=False)
    print("Data exported to CSV.")
else:
    print("No data to save to CSV.")








#2ND WAY

# import time
# from datetime import datetime
# import re
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from random import randint
# from win10toast import ToastNotifier
# import pandas as pd
# from selenium.common.exceptions import ElementClickInterceptedException
# from timeit import default_timer as timer

# class ScrapearGMaps:
    
#     data = pd.DataFrame(columns=['name', 'address', 'timetable'])
    
#     def __init__(self):
#         firefox_options = webdriver.FirefoxOptions()
#         firefox_options.set_preference("dom.webnotifications.enabled", False)
#         self.driver = webdriver.Firefox(options=firefox_options)  # Provide the correct path to geckodriver if it's not in the PATH
#         self.driver.maximize_window()
        
#     # ... (rest of the class methods)

# # ... (rest of the script)

        
#     def get_data(self): return self.data

#     def set_data(self, new_data): self.data = new_data

#     def push_notification(self, text):
#         toaster = ToastNotifier()
#         toaster.show_toast("Google Maps Scraper", text)

#     def scroll_the_page(self, i):
#         try:
#             section_loading = WebDriverWait(self.driver, 120).until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'wo1ice-loading')]")))
#             while True:
#                 if i >= len(WebDriverWait(self.driver, 120).until(
#                     EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'section-scrollbox')]//descendant::a")))):
#                     actions = ActionChains(self.driver)
#                     actions.move_to_element(section_loading).perform()
#                     time.sleep(randint(2, 3))
#                 else:
#                     break
#         except:
#             pass
        
#     def get_geocoder(self, url_location):
#         try:
#             coords = re.search(r"!3d-?\d\d?\.\d{4,8}!4d-?\d\d?\.\d{4,8}", url_location).group()
#             coord = coords.split('!3d')[1]
#             return tuple(coord.split('!4d'))
#         except (TypeError, AttributeError):
#             return ("", "")
        
#     def get_name(self):
#         try:
#             return WebDriverWait(self.driver, 2).until(
#                 EC.presence_of_element_located((By.XPATH, "//h1[contains(@class,'header-title')]//descendant::span"))).text
#         except:
#             return ""

#     def get_address(self):
#         try:
#             return WebDriverWait(self.driver, 2).until(
#                 EC.presence_of_element_located((By.XPATH, "//button[contains(@data-item-id,'address')]//div[contains(@class,'gm2-body-2')]"))).text
#         except:
#             return ""
        
#     def click_open_close_time(self):
#         try:
#             button = WebDriverWait(self.driver, 2).until(
#                 EC.element_to_be_clickable((By.XPATH, "//div//img[contains(@aria-label,'Hours')]")))
#             button.click()            
#         except Exception as e:
#             print(e)
    
#     def get_timetable(self):
#         try:
#             df_result = pd.DataFrame(columns=['day', 'open_time'])
#             week_days = WebDriverWait(self.driver, 2).until(
#                 EC.presence_of_all_elements_located((By.XPATH, "//th//descendant::div")))
#             week_days = list(filter(lambda a: week_days.index(a) % 2 == 0, week_days))

#             open_time = WebDriverWait(self.driver, 2).until(
#                 EC.presence_of_all_elements_located((By.XPATH, "//td//descendant::ul//li")))

#             if len(week_days) >= 7 and len(open_time) >= 7:
#                 for i in range(0, 7):
#                     day = week_days[i].get_attribute('innerHTML')
#                     time = open_time[i].get_attribute('innerHTML')
#                     df_result = df_result.append({'day': day, 'open_time': time}, ignore_index=True)
            
#             return df_result
#         except:
#             return ""
    
#     def scrape(self, query):
#         try:
#             query = query.replace(" ", "+")
#             url = f"https://www.google.com/maps/search/{query}/"
#             self.driver.get(url)
#             time.sleep(randint(2, 4))
            
#             while True:
#                 try:
#                     for i in range(0, 20):
#                         self.scroll_the_page(i)
#                         elements = WebDriverWait(self.driver, 120).until(
#                             EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'section-scrollbox')]//descendant::a")))
#                         element = elements[i]
#                         element.click()
#                         time.sleep(randint(2, 3))
#                         self.click_open_close_time()

#                         print("Scraping data for item " + str(i))    
#                         name = self.get_name()
#                         print("Name:", name)
#                         address = self.get_address()
#                         print("Address:", address)
#                         time_table = self.get_timetable()
#                         print("Timetable:", time_table)

#                         self.set_data(self.data.append({'name': name, 'address': address, 'timetable': time_table}, ignore_index=True))
                        
#                         # Save data to CSV after scraping each restaurant
#                         self.data.to_csv(query + "_data.csv", index=False)

#                         go_back_button = WebDriverWait(self.driver, 20).until(
#                             EC.presence_of_element_located((By.XPATH, "//button//span[contains(text(), 'Back to results')]")))
#                         go_back_button.click()
#                         time.sleep(randint(2, 4))
                    
#                     next_page = WebDriverWait(self.driver, 20).until(
#                         EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Next page']")))
#                     next_page.click()
#                     time.sleep(randint(3, 5))
#                 except ElementClickInterceptedException:
#                     self.push_notification("Oops! An error occurred")
#                     break
#         except Exception as e:
#             print(e)
        
#         time.sleep(5)
#         self.driver.quit()
#         self.push_notification("Data extraction for " + query.replace("+", " ") + " is complete.")
#         return self.data

# start = timer()
# start_time = datetime.now().time()
# query = "food+vendor+miami+usa"
# gmaps = ScrapearGMaps()
# print(gmaps.scrape(query))

# end_time = datetime.now().time()
# end = timer()
# print("Program execution time: " + str(end - start))
# print("Start time: " + str(start_time) + " - End time: " + str(end_time))


#3RD WAY

# import time
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class Business:
#     """Class to store business information."""
#     def __init__(self):
#         self.name = ""
#         self.address = ""
#         self.website = ""
#         self.phone_number = ""
#         self.reviews_average = ""
#         self.reviews_count = ""
#         self.latitude = 0.0
#         self.longitude = 0.0

# class BusinessList:
#     """Class to hold a list of Business objects and save to Excel and CSV."""
#     def __init__(self):
#         self.business_list = []

#     def dataframe(self):
#         """Transform business_list to pandas dataframe."""
#         return pd.json_normalize(
#             (vars(business) for business in self.business_list), sep="_"
#         )

#     def save_to_excel(self, filename):
#         """Save pandas dataframe to Excel (xlsx) file."""
#         self.dataframe().to_excel(f"{filename}.xlsx", index=False)

#     def save_to_csv(self, filename):
#         """Save pandas dataframe to CSV file."""
#         self.dataframe().to_csv(f"{filename}.csv", index=False)

# def extract_coordinates_from_url(url: str) -> tuple[float, float]:
#     """Helper function to extract coordinates from the URL."""
#     coordinates = url.split('/@')[-1].split('/')[0]
#     # Return latitude, longitude
#     return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])

# def scrape_restaurant_data(query, total):
#     business_list = BusinessList()

#     # Set up Chrome webdriver
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         # Navigate to Google Maps
#         driver.get("https://www.google.com/maps/search/food+vendor+miami+usa/@25.7825389,-80.3118612,12z/data=!3m1!4b1?entry=ttu")

#         # Wait for the search box to load
#         search_box = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "searchboxinput"))
#         )

#         # Enter the search query
#         search_box.clear()
#         search_box.send_keys(query)
#         search_box.submit()

#         # Wait for the listings to load
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "section-result"))
#         )

#         # Get the listings
#         listings = driver.find_elements(By.CLASS_NAME, "section-result")[:total]

#         for listing in listings:
#             try:
#                 listing.click()
#                 time.sleep(5)  # Wait for the details page to load

#                 business = Business()

#                 # Extract business information
#                 business.name = driver.find_element(By.CLASS_NAME, "section-hero-header-title").text
#                 business.reviews_average = driver.find_element(By.CLASS_NAME, "section-rating-count").text
#                 business.address = driver.find_element(By.CLASS_NAME, "section-info-line").text

#                 # Extract latitude and longitude
#                 business.latitude, business.longitude = extract_coordinates_from_url(driver.current_url)

#                 # Append the business object to the list
#                 business_list.business_list.append(business)

#                 print(f"Scraped data for: {business.name}")

#             except Exception as e:
#                 print(f"Error scraping data: {e}")

#             finally:
#                 # Go back to the search results
#                 driver.execute_script("window.history.go(-1)")
#                 time.sleep(3)  # Wait for the search results to load

#     finally:
#         # Save data to Excel and CSV
#         business_list.save_to_excel("restaurant_data")
#         business_list.save_to_csv("restaurant_data")

#         # Close the browser window
#         driver.quit()

# if __name__ == "__main__":
#     query = "food vendor miami usa"
#     total_listings = 1  # Set the number of listings to scrape

#     scrape_restaurant_data(query, total_listings)