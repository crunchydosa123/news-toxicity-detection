import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Define the minimum length for links
min_length = len("https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen30e02")

# Array with domain names to replace
domains = ["thehindu.com", "newindianexpress.com", "news18.com"]

def extract_and_write_links(keywords):
    driver = webdriver.Chrome()
    articles = []

    # Iterate over each domain and keyword
    for domain in domains:
        for keyword in keywords:
            # Construct the URL using the current keyword and domain
            url = f"https://news.google.com/search?q={keyword}%20india%20site%3A{domain}%20when%3A1d&hl=en-IN&gl=IN&ceid=IN%3Aen"
            print(f"Extracting links from {url}")
            driver.get(url)
            time.sleep(5)  # Allow time for the page to load

            # Find all <a> tags containing article links
            links = driver.find_elements(By.XPATH, '//a[@href]')

            # Extract href and text
            count = 0
            for link in links:
                if count >= 15:
                    break  # Limit to top 15 links
                
                href = link.get_attribute('href')
                text = link.text.strip()
                if href and text and len(href) > min_length:
                    articles.append((text, href))  # Store as a tuple
                    count += 1

    driver.quit()
    return articles  # Return the list of articles
