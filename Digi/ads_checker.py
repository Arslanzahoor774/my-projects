import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time 
# chrome_options = Options()
# chrome_options.add_argument("--headless")   
# chrome_options.add_argument("--start-maximized")  
# chrome_options.add_argument("--disable-gpu")  
# chrome_options.add_argument("--no-sandbox")  

# driver = webdriver.Chrome()

# # Function to check ads running status
# def check_ads(website_name):
#     driver.get("https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&q=%22veronicabeard.com%22&search_type=keyword_exact_phra")
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Clear']")))

#     clear_button = driver.find_element(By.XPATH, "//div[@aria-label='Clear']")
#     clear_button.click()
   
#     time.sleep(1)
#     search_field = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search by keyword or advertiser']"))
#     )

#     search_field.send_keys(website_name)
#     time.sleep(2)

#     suggestion_xpath = f"//div[@class='x12nagc']//span[contains(text(), '{website_name}')]"

#     try:
#         suggestion = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, suggestion_xpath))
#         )
#         suggestion.click()

#         time.sleep(3)

#         # Now, scrape the number of results
#         try:
#             results_element = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//div[@aria-level='3' and contains(@class, 'x8t9es0')]"))
#             )
#             results_text = results_element.text

#             # Use a regex to extract the number of results
#             match = re.search(r'~(\d+) results', results_text)
#             if match:
#                 num_results = int(match.group(1))
#                 # Determine if ads are running
#                 ads_running = "Yes" if num_results > 0 else "No"
#                 return ads_running, num_results
#             else:
#                 return "No", 0
#         except Exception as e:
#             print(f"Error while scraping results: {str(e)}")
#             return "No", 0
#     except Exception as e:
#         print(f"Error: Could not find suggestion for {website_name}. Exception: {str(e)}")
#         return "No", 0

# # Function to process websites from a CSV
# def process_websites(input_csv, output_csv):
#     # Open the input CSV file and the output CSV file
#     with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
#          open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        
#         reader = csv.reader(infile)
#         writer = csv.writer(outfile)
        
#         # Write the header row to the output CSV
#         writer.writerow(['Website URL', 'Ads Running (Yes/No)', 'Number of Ads'])

#         # Skip the header in the input file
#         next(reader)

#         # Process each website URL
#         for row in reader:
#             website_name = row[0]  # Assuming the URL is in the first column
#             print(f"Checking ads for: {website_name}")
            
#             # Check if ads are running and get the number of ads
#             ads_running, num_ads = check_ads(website_name)
            
#             # Write the results to the output CSV
#             writer.writerow([website_name, ads_running, num_ads])
#             print(f"Processed {website_name}: {ads_running} ({num_ads} ads)")

# # Run the script
# input_csv = "Lenob _ Lead Gen Batch 1  - Sheet14.csv"  # Path to your input CSV file with websites
# output_csv = "output_ads_results.csv"  # Path to the output CSV file

# # Process websites
# process_websites(input_csv, output_csv)

# # Close the browser after processing
# driver.quit()
import csv
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Selenium setup
chrome_options = Options()
chrome_options.add_argument("--headless")   
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

# Function to check ads running status
def check_ads(website_name):
    driver.get("https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&is_targeted_country=false&media_type=all&q=%22veronicabeard.com%22&search_type=keyword_exact_phra")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Clear']")))

    clear_button = driver.find_element(By.XPATH, "//div[@aria-label='Clear']")
    clear_button.click()

    time.sleep(1)
    search_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search by keyword or advertiser']"))
    )

    search_field.send_keys(website_name)
    time.sleep(1)

    suggestion_xpath = f"//div[@class='x12nagc']//span[contains(text(), '{website_name}')]"

    try:
        suggestion = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, suggestion_xpath))
        )
        suggestion.click()

        time.sleep(3)

        # Scrape the number of results
        try:
            results_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-level='3' and contains(@class, 'x8t9es0')]"))
            )
            results_text = results_element.text

            # Use a regex to extract the number of results
            match = re.search(r'~(\d+) results', results_text)
            if match:
                num_results = int(match.group(1))
                ads_running = "Yes" if num_results > 0 else "No"
                return ads_running, num_results
            else:
                return "No", 0
        except Exception as e:
            print(f"Error while scraping results: {str(e)}")
            return "No", 0
    except Exception as e:
        print(f"Error: Could not find suggestion for {website_name}. Exception: {str(e)}")
        return "No", 0

# Function to process websites from a CSV
def process_websites(input_csv, output_csv):
    try:
        with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
             open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            writer.writerow(['Website URL', 'Ads Running (Yes/No)', 'Number of Ads'])

            next(reader)

            for row in reader:
                website_name = row[0]
                print(f"Checking ads for: {website_name}")

                ads_running, num_ads = check_ads(website_name)

                writer.writerow([website_name, ads_running, num_ads])
                print(f"Processed {website_name}: {ads_running} ({num_ads} ads)")

        messagebox.showinfo("Success", f"Processing complete. Results saved to: {output_csv}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# GUI Implementation
def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        input_file_path.set(file_path)
    else:
        messagebox.showwarning("Invalid Selection", "Please select a valid CSV file.")

def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_path.set(folder_path)

def start_processing():
    input_file = input_file_path.get()
    output_folder = output_folder_path.get()

    if not input_file:
        messagebox.showwarning("No Input File", "Please select an input file first.")
        return

    if not input_file.endswith(".csv"):
        messagebox.showwarning("Invalid File", "Selected file is not a CSV. Please select a valid CSV file.")
        return

    output_file = os.path.join(output_folder if output_folder else os.path.expanduser("~/Desktop"), "output_ads_results.csv")

    process_websites(input_file, output_file)

# Initialize Tkinter
root = tk.Tk()
root.title("Ads Checker Tool")

input_file_path = tk.StringVar()
output_folder_path = tk.StringVar()

# UI Elements
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Select Input CSV File:").grid(row=0, column=0, sticky="w")
input_button = tk.Button(frame, text="Select File", command=select_input_file)
input_button.grid(row=0, column=1, padx=5)

input_entry = tk.Entry(frame, textvariable=input_file_path, width=50)
input_entry.grid(row=0, column=2, padx=5)

tk.Label(frame, text="Select Output Folder:").grid(row=1, column=0, sticky="w")
output_button = tk.Button(frame, text="Select Folder", command=select_output_folder)
output_button.grid(row=1, column=1, padx=5)

output_entry = tk.Entry(frame, textvariable=output_folder_path, width=50)
output_entry.grid(row=1, column=2, padx=5)

start_button = tk.Button(frame, text="Start Processing", command=start_processing)
start_button.grid(row=2, column=0, columnspan=3, pady=10)

# Run the GUI loop
root.mainloop()

# Close the browser after the GUI closes
driver.quit()
