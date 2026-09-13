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



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Set up WebDriver (replace 'path/to/chromedriver' with your actual path)
driver = webdriver.Chrome(executable_path='D:/Chrome Driver/chromedriver-win64/chromedriver.exe')

# Navigate to the Google Maps link
driver.get('https://www.google.com/maps/search/food+vendor+miami+usa/@25.8105409,-80.3449814,12z?entry=ttu')

# Wait for the page to load
time.sleep(5)

# Initialize lists to store data
names = []
addresses = []
review_counts = []
directions = []

# Loop through the top 10 results
for i in range(1, 11):
    # Click on the restaurant
    restaurant_xpath = f'//div[@class="section-result"][{i}]'
    driver.find_element(By.XPATH, restaurant_xpath).click()
    
    # Wait for the details page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-hero-header-title")))
    time.sleep(2)  # Adding a short delay for stability
    
    # Extract restaurant details
    name = driver.find_element(By.CLASS_NAME, "section-hero-header-title").text
    address = driver.find_element(By.CLASS_NAME, "section-info-line").text
    review_count = driver.find_element(By.CLASS_NAME, "section-rating-count").text
    direction = driver.find_element(By.CLASS_NAME, "section-directions-travel-modes").text
    
    # Append data to lists
    names.append(name)
    addresses.append(address)
    review_counts.append(review_count)
    directions.append(direction)
    
    # Go back to the search results page
    driver.execute_script("window.history.go(-1)")
    
    # Wait for the search results page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-result")))
    time.sleep(2)  # Adding a short delay for stability

# Create a DataFrame from the lists
data = {'Name': names, 'Address': addresses, 'Review Count': review_counts, 'Direction': directions}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('restaurant_data.csv', index=False)

# Close the browser window
driver.quit()

