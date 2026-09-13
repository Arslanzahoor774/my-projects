
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.firefox import GeckoDriverManager
# from collections import Counter
# import time
# import re

# # Set up Firefox options
# options = webdriver.FirefoxOptions()
# options.headless = False  # Set to True if you want to run in headless mode

# # Instantiate the WebDriver using WebDriverManager
# driver = webdriver.Firefox(service=webdriver.FirefoxService(executable_path=GeckoDriverManager().install()), options=options)

# # Wait for the page to load (wait for tweets to be present)
# driver.get("https://twitter.com/explore")
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# # Check if the login prompt is present
# login_prompt_present = EC.presence_of_element_located((By.XPATH, '//div[@data-testid="login"]'))
# if login_prompt_present(driver):
#     # Find the login elements and enter credentials
#     login_username = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.NAME, 'session[username_or_email]'))
#     )
#     login_password = driver.find_element(By.NAME, 'session[password]')

#     login_username.send_keys('arslanzahoor774@gmail.com')  # Replace with your Twitter username
#     login_password.send_keys('Arslan12362')  # Replace with your Twitter password

#     login_password.send_keys(Keys.RETURN)

#     # Wait for the page to load after login
#     WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# # Find the search box and search for a term (e.g., "#")
# search_box = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Search query"]'))
# )
# search_box.send_keys('#')
# search_box.send_keys(Keys.RETURN)

# # Wait for search results to load (wait for tweets to be present)
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# # Scroll to load more tweets (adjust the range as needed)
# for _ in range(10):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)

# # Find tweets and extract hashtags
# tweets = driver.find_elements_by_xpath('//div[@data-testid="tweetText"]')
# all_hashtags = []
# for tweet in tweets:
#     all_hashtags.extend(re.findall(r'#\w+', tweet.text.lower()))

# # Count hashtags
# top_hashtags = Counter(all_hashtags).most_common(10)

# # Print top 10 hashtags
# for tag, count in top_hashtags:
#     print(f"#{tag}: {count} posts")

# # Store the data in a CSV file
# csv_filename = 'twitter_top_hashtags.csv'
# with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
#     fieldnames = ['Hashtag', 'Post Count']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#     # Write the header
#     writer.writeheader()

#     # Write the data
#     for tag, count in top_hashtags:
#         writer.writerow({'Hashtag': tag, 'Post Count': count})

# print(f'Data has been stored in {csv_filename}.')

# # Close the browser
# driver.quit()


# import csv
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.firefox import GeckoDriverManager
# from collections import Counter
# import time

# # Set up Firefox options
# options = webdriver.FirefoxOptions()
# options.headless = False  # Set to True if you want to run in headless mode

# # Instantiate the WebDriver using WebDriverManager
# driver = webdriver.Firefox(service=webdriver.FirefoxService(executable_path=GeckoDriverManager().install()), options=options)

# # Provide Twitter credentials
# twitter_email = "arslanzahoor774@gmail.com"
# twitter_password = "Arslan12362"

# # Wait for the page to load (wait for tweets to be present)
# driver.get("https://twitter.com/explore")
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# # Check if the login prompt is present
# login_prompt_present = EC.presence_of_element_located((By.XPATH, '//div[@data-testid="login"]'))
# if login_prompt_present(driver):
#     # Find the login elements and enter credentials
#     login_username = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.NAME, 'session[username_or_email]'))
#     )
#     login_password = driver.find_element(By.NAME, 'session[password]')

#     login_username.send_keys(twitter_email)
#     login_password.send_keys(twitter_password)
#     login_password.send_keys(Keys.RETURN)

#     # Wait for the page to load after login
#     WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# # Find the search box and search for a term (e.g., "#")
# search_box = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Search query"]'))
# )
# search_box.send_keys('#')
# search_box.send_keys(Keys.RETURN)

# # Wait for search results to load (wait for tweets to be present)
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# # Scroll to load more tweets (adjust the range as needed)
# for _ in range(10):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)

# # Find tweets and extract hashtags
# tweets = driver.find_elements_by_xpath('//div[@data-testid="tweetText"]')
# all_hashtags = []
# for tweet in tweets:
#     all_hashtags.extend(re.findall(r'#\w+', tweet.text.lower()))

# # Count hashtags
# top_hashtags = Counter(all_hashtags).most_common(10)

# # Print top 10 hashtags
# for tag, count in top_hashtags:
#     print(f"#{tag}: {count} posts")

# # Store the data in a CSV file
# csv_filename = 'twitter_top_hashtags.csv'
# with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
#     csv_writer = csv.writer(csv_file)
    
#     # Write the header
#     csv_writer.writerow(['Hashtag', 'Post Count'])

#     # Write the data
#     csv_writer.writerows(top_hashtags)

# print(f'Data has been stored in {csv_filename}.')

# # Close the browser
# driver.quit()

#FOR TOP 5 HASHTAGS
# import csv
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.firefox import GeckoDriverManager
# from collections import Counter
# import time

# # Set up Firefox options
# options = webdriver.FirefoxOptions()
# options.headless = False  # Set to True if you want to run in headless mode

# # Instantiate the WebDriver using WebDriverManager
# driver = webdriver.Firefox(service=webdriver.FirefoxService(executable_path=GeckoDriverManager().install()), options=options)

# # Provide Twitter credentials
# twitter_email = "arslanzahoor774@gmail.com"
# twitter_password = "Arslan12362"

# # Wait for the page to load (wait for tweets to be present)
# driver.get("https://twitter.com/explore")
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# # Check if the login prompt is present
# login_prompt_present = EC.presence_of_element_located((By.XPATH, '//div[@data-testid="login"]'))
# if login_prompt_present(driver):
#     # Find the login elements and enter credentials
#     login_username = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.NAME, 'session[username_or_email]'))
#     )
#     login_password = driver.find_element(By.NAME, 'session[password]')

#     login_username.send_keys(twitter_email)
#     login_password.send_keys(twitter_password)
#     login_password.send_keys(Keys.RETURN)

#     # Wait for the page to load after login
#     WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# # Find the search box and search for a term (e.g., "#")
# search_box = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Search query"]'))
# )
# search_box.send_keys('#')
# search_box.send_keys(Keys.RETURN)

# # Wait for search results to load (wait for tweets to be present)
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# # Scroll to load more tweets (adjust the range as needed)
# for _ in range(10):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)

# # Find tweets and extract hashtags
# tweets = driver.find_elements_by_xpath('//div[@data-testid="tweetText"]')
# all_hashtags = []
# for tweet in tweets:
#     all_hashtags.extend(re.findall(r'#\w+', tweet.text.lower()))

# # Count hashtags
# top_hashtags = Counter(all_hashtags).most_common(5)

# # Print top 5 hashtags
# for tag, count in top_hashtags:
#     print(f"#{tag}: {count} posts")

# # Store the data in a CSV file
# csv_filename = 'twitter_top_hashtags.csv'
# with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
#     csv_writer = csv.writer(csv_file)
    
#     # Write the header
#     csv_writer.writerow(['Hashtag', 'Post Count'])

#     # Write the data
#     csv_writer.writerows(top_hashtags)

# print(f'Data has been stored in {csv_filename}.')

# # Close the browser
# driver.quit()


#FOR CONSOLE DATA
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from collections import Counter
import time

# Set up Firefox options
options = webdriver.FirefoxOptions()
options.headless = False  # Set to True if you want to run in headless mode

# Instantiate the WebDriver using WebDriverManager
driver = webdriver.Firefox(service=webdriver.FirefoxService(executable_path=GeckoDriverManager().install()), options=options)

# Provide Twitter credentials
twitter_email = "arslanzahoor774@gmail.com"
twitter_password = "Arslan12362"

# Wait for the page to load (wait for tweets to be present)
driver.get("https://twitter.com/explore")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# Check if the login prompt is present
login_prompt_present = EC.presence_of_element_located((By.XPATH, '//div[@data-testid="login"]'))
if login_prompt_present(driver):
    # Find the login elements and enter credentials
    login_username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, 'session[username_or_email]'))
    )
    login_password = driver.find_element(By.NAME, 'session[password]')

    login_username.send_keys(twitter_email)
    login_password.send_keys(twitter_password)
    login_password.send_keys(Keys.RETURN)

    # Wait for the page to load after login
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# Find the search box and search for a term (e.g., "#")
search_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Search query"]'))
)
search_box.send_keys('#')
search_box.send_keys(Keys.RETURN)

# Wait for search results to load (wait for tweets to be present)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

# Scroll to load more tweets (adjust the range as needed)
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Find tweets and extract hashtags
tweets = driver.find_elements_by_xpath('//div[@data-testid="tweetText"]')
all_hashtags = []
for tweet in tweets:
    all_hashtags.extend(re.findall(r'#\w+', tweet.text.lower()))

# Count hashtags
top_hashtags = Counter(all_hashtags).most_common(5)

# Print top 5 hashtags to the console
for tag, count in top_hashtags:
    print(f"#{tag}: {count} posts")

# Close the browser
driver.quit()
