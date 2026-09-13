
# from selenium import webdriver
# from webdriver_manager.firefox import GeckoDriverManager
# import time

# # Your Facebook credentials
# username = "arslanzahoor774@gmail.com"
# password = "Arslan12362"

# # Set up Firefox options
# options = webdriver.FirefoxOptions()
# options.headless = True  # Run in headless mode


# # Instantiate the WebDriver using WebDriverManager
# driver = webdriver.Firefox(service=webdriver.FirefoxService(executable_path=GeckoDriverManager().install()), options=options)

# # Open Facebook
# driver.get("https://www.facebook.com")

# # Log in
# email_field = driver.find_element_by_id("email")
# password_field = driver.find_element_by_id("pass")
# login_button = driver.find_element_by_id("loginbutton")

# email_field.send_keys(username)
# password_field.send_keys(password)
# login_button.click()

# # Navigate to the birthday page
# driver.get("https://www.facebook.com/events/birthdays/")

# # Find the textarea for posting
# post_textarea = driver.find_element_by_css_selector("div[role='textbox']")

# # Write your birthday message
# birthday_message = "Happy Birthday! 🎉🥳"
# post_textarea.send_keys(birthday_message)

# # Post the message
# post_button = driver.find_element_by_css_selector("div[aria-label='Post']")
# post_button.click()

# # Close the browser
# # Wait for a longer time to allow the post to be processed
# time.sleep(10)  # Adjust the sleep duration as needed
# driver.quit()


from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import requests

# Your Facebook credentials
username = "arslanzahoor774@gmail.com"
password = "Arslan12362"

# Your 2Captcha API Key
captcha_api_key = "YOUR_2CAPTCHA_API_KEY"

# Set up Firefox options
options = webdriver.FirefoxOptions()
options.headless = False  # Set to True for headless mode

# Instantiate the WebDriver using WebDriverManager
driver = webdriver.Firefox(service=webdriver.FirefoxService(executable_path=GeckoDriverManager().install()), options=options)

# Open Facebook
driver.get("https://www.facebook.com")

# Log in
email_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "email")))
password_field = driver.find_element(By.ID, "pass")
login_button = driver.find_element(By.NAME, "login")

email_field.send_keys(username)
password_field.send_keys(password)

try:
    # Check if CAPTCHA is present
    captcha_image = driver.find_element(By.XPATH, "//img[@alt='captcha']")
    captcha_text = solve_captcha(captcha_image, captcha_api_key)
    captcha_input = driver.find_element(By.NAME, "captcha_response")
    captcha_input.send_keys(captcha_text)
except NoSuchElementException:
    pass  # No CAPTCHA present, continue with login

login_button.click()

try:
    # Wait for the Facebook homepage to load
    wait = WebDriverWait(driver, 30)  # Increased timeout
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/me/')]")))
    print("Login successful, navigated to homepage.")

    # Navigate to the Events (birthday) page
    driver.get("https://www.facebook.com/events/birthdays/")

    try:
        # Wait for the Events (birthday) page to load
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Birthdays')]")))
        print("Navigated to the Events (birthday) page.")
    except TimeoutException:
        print("Failed to navigate to the Events (birthday) page.")
        driver.quit()
        exit()

    # Add a delay to ensure page loads
    time.sleep(5)

    # Find all friends with birthdays
    birthday_friends = driver.find_elements(By.XPATH, "//div[contains(@class, 'birthdays')]//textarea")

    # Post birthday wishes
    for textarea in birthday_friends:
        textarea.send_keys("Happy Birthday! 🎉🥳")
        time.sleep(2)  # Adjust time as needed
        post_button = textarea.find_element(By.XPATH, "./following-sibling::div/button")
        post_button.click()
        time.sleep(2)  # Adjust time as needed

    print("Birthday wishes posted successfully.")

except TimeoutException:
    print("Failed to navigate to the homepage or Events (birthday) page. Check the login process or page structure.")

# Close the browser
driver.quit()
