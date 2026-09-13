# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.common.by import By
# import time

# # Replace with your LinkedIn login credentials
# linkedin_email = 'arslanzahoor774@gmail.com'
# linkedin_password = 'Arslan12362'

# # Replace with the URL of the LinkedIn profile
# linkedin_profile_url = 'https://www.linkedin.com/in/muhammad-arslan-zahoor-1a8bb120a/'

# # Specify the path to the Chrome WebDriver executable
# chrome_driver_path = 'D:\Chrome Driver\chromedriver-win64/chromedriver.exe'

# # Set up Chrome WebDriver options
# chrome_options = ChromeOptions()
# chrome_options.add_argument('--start-maximized')  # Optional: Start Chrome in maximized mode

# # Initialize Chrome WebDriver with the specified options and driver path
# driver = webdriver.Chrome(service=ChromeService(executable_path=chrome_driver_path), options=chrome_options)

# # Log in to LinkedIn
# driver.get('https://www.linkedin.com/')
# time.sleep(2)  # Adjust the sleep time as needed
# driver.find_element(By.NAME, 'session_key').send_keys(linkedin_email)
# driver.find_element(By.NAME, 'session_password').send_keys(linkedin_password)
# time.sleep(2)  # Adjust the sleep time as needed
# driver.find_element(By.CLASS_NAME, 'sign-in-form__submit-btn--full-width').click()

# # Wait for login to complete (you may need to adjust the waiting time)
# time.sleep(6)

# # Navigate to the LinkedIn profile URL
# driver.get(linkedin_profile_url)
# time.sleep(2)  # Adjust the sleep time as needed

# # Define a function to extract profile information
# def extract_profile_info():
#     # Extract profile name
#     profile_name = driver.find_element(By.CLASS_NAME, 'pv-top-card--list').find_element(By.TAG_NAME, 'li').text.strip()
    
#     # Extract profile URL
#     profile_url = driver.current_url
    
#     # Scroll down to load more information on the profile page
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)  # Adjust the sleep time as needed
    
#     # Extract about information
#     about_element = driver.find_element(By.CLASS_NAME, 'pv-about-section')
#     about_info = about_element.find_element(By.CLASS_NAME, 'pv-about__summary-text').text.strip()
    
#     return {
#         'Profile Name': profile_name,
#         'Profile URL': profile_url,
#         'About Information': about_info
#     }

# # Extract profile information
# profile_info = extract_profile_info()

# # Close the WebDriver when done
# driver.quit()

# # Print the extracted profile information
# print(f'Profile Name: {profile_info["Profile Name"]}')
# print(f'Profile URL: {profile_info["Profile URL"]}')
# print(f'About Information: {profile_info["About Information"]}')

#BREAK
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# Replace with your LinkedIn login credentials
linkedin_email = 'arslanzahoor774@gmail.com'
linkedin_password = 'Arslan12362'

# Replace with the URL of the LinkedIn profile
linkedin_profile_url = 'https://www.linkedin.com/in/muhammad-arslan-zahoor-1a8bb120a/'

# Specify the path to the Chrome WebDriver executable
chrome_driver_path = 'D:/Chrome Driver/chromedriver-win64/chromedriver.exe'  # Adjust the path

# Set up Chrome WebDriver options
chrome_options = ChromeOptions()
chrome_options.add_argument('--start-maximized')  # Optional: Start Chrome in maximized mode

# Initialize Chrome WebDriver with the specified options and driver path
driver = webdriver.Chrome(service=ChromeService(executable_path=chrome_driver_path), options=chrome_options)

# Log in to LinkedIn
driver.get('https://www.linkedin.com/')
time.sleep(2)  # Adjust the sleep time as needed
driver.find_element(By.NAME, 'session_key').send_keys(linkedin_email)
driver.find_element(By.NAME, 'session_password').send_keys(linkedin_password)
time.sleep(2)  # Adjust the sleep time as needed
driver.find_element(By.CLASS_NAME, 'sign-in-form__submit-btn--full-width').click()

# Wait for login to complete (you may need to adjust the waiting time)
time.sleep(6)

# Navigate to the LinkedIn profile URL
driver.get(linkedin_profile_url)
time.sleep(2)  # Adjust the sleep time as needed

# Define a function to extract profile information
def extract_profile_info():
    try:
        # Wait for the profile information to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pv-top-card--list'))
        )

        # Extract profile name
        profile_name = driver.find_element(By.CLASS_NAME, 'pv-top-card--list').find_element(By.TAG_NAME, 'li').text.strip()
        
        # Extract profile URL
        profile_url = driver.current_url
        
        # Scroll down to load more information on the profile page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed
        
        # Extract about information
        about_element = driver.find_element(By.CLASS_NAME, 'pv-about-section')
        about_info = about_element.find_element(By.CLASS_NAME, 'pv-about__summary-text').text.strip()
        
        return {
            'Profile Name': profile_name,
            'Profile URL': profile_url,
            'About Information': about_info
        }
    except NoSuchElementException as e:
        print(f"Error extracting profile information: {e}")
        return None


# Extract profile information
profile_info = extract_profile_info()

# Close the WebDriver when done
driver.quit()

# Print the extracted profile information
if profile_info:
    print(f'Profile Name: {profile_info["Profile Name"]}')
    print(f'Profile URL: {profile_info["Profile URL"]}')
    print(f'About Information: {profile_info["About Information"]}')
else:
    print("Failed to extract profile information.")

# Store the data in a CSV file
csv_filename = 'linkedin_profile_info.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Profile Name', 'Profile URL', 'About Information']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    if profile_info:
        writer.writerow(profile_info)

print(f'Data has been stored in {csv_filename}.')
