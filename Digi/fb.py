from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Your Facebook credentials
username = "arslanzahoor7774@gmail.com"
password = "Arslan12362"

# Initialize the webdriver (you need to download the appropriate driver for your browser)
driver = webdriver.Chrome("C:\ProgramData\Microsoft\Windows\Start Menu\Programs")

# Open Facebook
driver.get("https://www.facebook.com")

# Log in
email_field = driver.find_element_by_id("email")
password_field = driver.find_element_by_id("pass")
login_button = driver.find_element_by_id("loginbutton")

email_field.send_keys(username)
password_field.send_keys(password)
login_button.click()

# Navigate to the birthday page
driver.get("https://www.facebook.com/events/birthdays/")

# Find the textarea for posting
post_textarea = driver.find_element_by_css_selector("div[role='textbox']")

# Write your birthday message
birthday_message = "Happy Birthday! 🎉🥳"
post_textarea.send_keys(birthday_message)

# Post the message
post_button = driver.find_element_by_css_selector("div[aria-label='Post']")
post_button.click()

# Close the browser
time.sleep(5)  # Give it some time to post
driver.quit()
