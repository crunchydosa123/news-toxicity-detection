import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Define the minimum length for links
min_length = len("https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen30e02")

# Array with domain names to replace
domains = ["thehindu.com", "newindianexpress.com", "news18.com"]

# Array with keywords to replace
keywords = ["murder", "rape", "terror", "victory"]

# Set up the Selenium WebDriver (e.g., Chrome)
driver = webdriver.Chrome()

# Function to extract links and write to CSV
def extract_and_write_links(url, writer):
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load

    # Find all <a> tags containing article links
    links = driver.find_elements(By.XPATH, '//a[@href]')

    # Extract href and text, and write them to the CSV file, filtering out empty text elements
    count = 0
    for link in links:
        if count >= 15:
            break  # Limit to top 15 links
        
        href = link.get_attribute('href')
        text = link.text.strip()
        if href and text and len(href) > min_length:  # Check if both href and text are not empty and href is long enough
            writer.writerow([text, href])
            count += 1

# Open the CSV file for writing
with open('gnews_links2.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write the header row
    writer.writerow(['Text', 'Link'])

    # Iterate over each domain and keyword
    for domain in domains:
        for keyword in keywords:
            # Construct the URL using current keyword and domain
            url = f"https://news.google.com/search?q={keyword}%20india%20site%3A{domain}%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen"
            print(f"Extracting links from {url}")
            extract_and_write_links(url, writer)

# Close the browser after scraping
driver.quit()

print("Scraping completed and saved to 'gnews_links.csv'.")
