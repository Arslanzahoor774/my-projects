# import tweepy
# from collections import Counter

# # Replace these with your Twitter API credentials
# api_key = 'HN2uBzzTnJLEUaA1ULbSJ0QhP'
# api_secret_key = 'p4QSpK9q5ddDyyKTk6mgAHc1jkdqR1oaoAVWtbAihhTxsi9IWS'
# access_token = '1715397039247499264-rDmZR4f2zvN6td9l9zhX8U7ODBSnzT'
# access_token_secret = 'UzRNAn66TADZPu9G2WtLZELTKF28x36kVUmtz9UKCgW7M'

# # Authenticate with the Twitter API
# auth = tweepy.OAuthHandler(api_key, api_secret_key)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)

# # Function to extract hashtags from tweets
# def extract_hashtags(tweets):
#     hashtags = []
#     for tweet in tweets:
#         hashtags.extend([hashtag['text'].lower() for hashtag in tweet.entities.get('hashtags', [])])
#     return hashtags

# try:
#     # Fetch tweets. Adjust the query parameters as needed
#     tweets = api.search_tweets(q="*", count=100, result_type="recent")

#     # Extract hashtags from tweets
#     hashtags = extract_hashtags(tweets)

#     # Count and get top 10 hashtags
#     top_hashtags = Counter(hashtags).most_common(10)

#     # Print top 10 hashtags and their counts
#     for tag, count in top_hashtags:
#         print(f"#{tag}: {count} posts")

# except tweepy.TweepyException as e:
#     print(f"An error occurred: {e}")


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from collections import Counter
import time
import re

# Set up the WebDriver path
gecko_driver_path = 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs/geckodriver.exe' # Replace with your GeckoDriver path

# Set up Firefox options
options = Options()

# Instantiate the WebDriver
driver = webdriver.Firefox(executable_path=gecko_driver_path, options=options)

# Function to extract hashtags from a string
def extract_hashtags(text):
    return re.findall(r'#\w+', text.lower())

try:
    # Open Twitter
    driver.get("https://twitter.com/explore")

    # Wait for the page to load
    time.sleep(5)

    # Find the search box and search for a term (e.g., "#")
    search_box = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
    search_box.send_keys('#')
    search_box.send_keys(Keys.RETURN)

    # Wait for search results to load
    time.sleep(5)

    # Scroll to load more tweets (adjust the range as needed)
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Find tweets and extract hashtags
    tweets = driver.find_elements_by_xpath('//div[@data-testid="tweetText"]')
    all_hashtags = []
    for tweet in tweets:
        all_hashtags.extend(extract_hashtags(tweet.text))

    # Count hashtags
    top_hashtags = Counter(all_hashtags).most_common(10)

    # Print top 10 hashtags
    for tag, count in top_hashtags:
        print(f"#{tag}: {count} posts")

finally:
    # Close the browser
    driver.quit()

