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
    
#     data = pd.DataFrame(columns=['name', 'address', 'phone_number', 'timetable'])
    
#     def __init__(self):
#         firefox_options = webdriver.FirefoxOptions()
#         firefox_options.set_preference("dom.webnotifications.enabled", False)
#         self.driver = webdriver.Firefox(options=firefox_options)  # Provide the correct path to geckodriver if it's not in the PATH
#         self.driver.maximize_window()
        
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
#                 print(len(WebDriverWait(self.driver, 120).until(
#                     EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'section-scrollbox')]//descendant::a")))))
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

#     def get_phone(self):
#         try:
#             phone_number = self.driver.find_element_by_css_selector(
#                 "[data-tooltip='Copy phone number']").get_attribute("aria-label")
#             return phone_number.replace("Phone: ", "")
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
#                         phone = self.get_phone()
#                         print("Phone Number:", phone)
#                         time_table = self.get_timetable()
#                         print("Timetable:", time_table)

#                         self.set_data(self.data.append({'name': name, 'address': address, 'phone_number': phone, 'timetable': time_table}, ignore_index=True))
                        
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
        
#         if not self.data.empty:
#             # Save data to CSV with formatted timetable
#             self.data['timetable'] = self.data['timetable'].apply(lambda x: "\n".join([f"{day}: {time}" for day, time in zip(x['day'], x['open_time'])]))
#             self.data.to_csv(query + "_data.csv", index=False)
#             self.push_notification("Data extraction for " + query.replace("+", " ") + " is complete.")
#         else:
#             print("No data scraped.")
        
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

#DRIVER FIREFOX

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

#DRIVER CHROME
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
# from chromedriver_autoinstaller import install as chromedriver_install

# class ScrapearGMaps:
    
#     data = pd.DataFrame(columns=['name', 'address', 'timetable'])
    
#     def __init__(self):
#         # Ensure that the ChromeDriver is installed and up-to-date
#         chromedriver_install()
        
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument('--headless')  # Add this line if you want to run Chrome in headless mode
#         self.driver = webdriver.Chrome(options=chrome_options)
#         self.driver.maximize_window()
        
    # ... (rest of the class methods)
#FOR LOOP DATA 

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

#FOR ONE ELEMENT DATA
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd
from timeit import default_timer as timer

class ScrapearGMaps:

    data = pd.DataFrame(columns=['name', 'address', 'timetable'])

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def get_data(self):
        return self.data

    def set_data(self, new_data):
        self.data = new_data

    def push_notification(self, text):
        print(text)

    def scroll_the_page(self, i):
        try:
            section_loading = WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'wo1ice-loading')]")))
            while True:
                if i >= len(WebDriverWait(self.driver, 120).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'section-scrollbox')]//descendant::a")))):
                    actions = ActionChains(self.driver)
                    actions.move_to_element(section_loading).perform()
                    time.sleep(randint(2, 4))
                else:
                    break
        except:
            pass

    def get_name(self):
        try:
            return WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(@class,'header-title')]//descendant::span"))).text
        except:
            return ""

    def get_address(self):
        try:
            return WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@data-item-id,'address')]//div[contains(@class,'gm2-body-2')]"))).text
        except:
            return ""

    def click_open_close_time(self):
        try:
            button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//div//img[contains(@aria-label,'Hours')]")))
            button.click()
        except Exception as e:
            print(e)

    def get_timetable(self):
        try:
            df_result = pd.DataFrame(columns=['day', 'open_time'])
            week_days = WebDriverWait(self.driver, 2).until(
                EC.presence_of_all_elements_located((By.XPATH, "//th//descendant::div")))
            week_days = list(filter(lambda a: week_days.index(a) % 2 == 0, week_days))

            open_time = WebDriverWait(self.driver, 2).until(
                EC.presence_of_all_elements_located((By.XPATH, "//td//descendant::ul//li")))

            if len(week_days) >= 7 and len(open_time) >= 7:
                for i in range(0, 7):
                    day = week_days[i].get_attribute('innerHTML')
                    time = open_time[i].get_attribute('innerHTML')
                    df_result = df_result.append({'day': day, 'open_time': time}, ignore_index=True)

            return df_result
        except:
            return ""

    def scrape(self, query):
        try:
            query = query.replace(" ", "+")
            url = f"https://www.google.com/maps/search/{query}/"
            self.driver.get(url)
            time.sleep(randint(2, 4))

            while True:
                try:
                    for i in range(0, 1):  # Scrape only the first result
                        self.scroll_the_page(i)
                        elements = WebDriverWait(self.driver, 120).until(
                            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'section-scrollbox')]//descendant::a")))
                        element = elements[i]
                        element.click()
                        time.sleep(randint(2, 3))
                        self.click_open_close_time()

                        print("Scraping data for item " + str(i))
                        name = self.get_name()
                        print("Name:", name)
                        address = self.get_address()
                        print("Address:", address)
                        time_table = self.get_timetable()
                        print("Timetable:", time_table)

                        self.set_data(self.data.append({'name': name, 'address': address, 'timetable': time_table},
                                                       ignore_index=True))

                        # Save data to CSV after scraping each restaurant
                        self.data.to_csv(query + "_data.csv", index=False)

                        go_back_button = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//button//span[contains(text(), 'Back to results')]")))
                        go_back_button.click()
                        time.sleep(randint(2, 4))

                    next_page = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Next page']")))
                    next_page.click()
                    time.sleep(randint(3, 5))
                except ElementClickInterceptedException:
                    self.push_notification("Oops! An error occurred")
                    break
        except Exception as e:
            print(e)

        time.sleep(5)
        self.driver.quit()
        self.push_notification("Data extraction for " + query.replace("+", " ") + " is complete.")
        return self.data

start = timer()
start_time = datetime.now().time()
query = "food+vendor+miami+usa"
gmaps = ScrapearGMaps()
print(gmaps.scrape(query))

end_time = datetime.now().time()
end = timer()
print("Program execution time: " + str(end - start))
print("Start time: " + str(start_time) + " - End time: " + str(end_time))

