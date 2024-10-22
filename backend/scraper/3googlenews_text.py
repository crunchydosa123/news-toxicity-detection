import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Function to extract text from <p> tags given a URL
def extract_paragraph_text(url, driver, timeout=30):
    driver.get(url)
    
    # Initialize WebDriverWait with a custom timeout
    wait = WebDriverWait(driver, timeout)
    
    try:
        # Wait for <p> tags to be present on the page
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
        
        # Check if <p> tags are present
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        if not paragraphs:
            print(f"No <p> tags found on page {url}")
            return "No <p> tags found"
        
        # Concatenate the text from <p> tags
        paragraph_text = ' '.join([para.text for para in paragraphs]).strip()
        
        return paragraph_text if paragraph_text else "No text found"
    
    except TimeoutException:
        print(f"Timeout loading page {url}")
        return "Timeout"
    
    except Exception as e:
        print(f"Error loading page {url}: {e}")
        return "Error loading page"

# Set up the Selenium WebDriver (e.g., Chrome)
driver = webdriver.Chrome()

# Open the CSV file with links and titles
with open('links2_unique.csv', mode='r', encoding='utf-8') as input_file:
    reader = csv.reader(input_file)
    
    # Skip the header row
    next(reader)
    
    # Open the new CSV file to save the extracted text
    with open('gnews_text2.csv', mode='w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        
        # Write the header row
        writer.writerow(['Title', 'Text'])

        # Read each row from the input CSV file
        for row in reader:
            title = row[0]  # Column 1: Title
            url = row[1]    # Column 2: Link
            
            if url:
                # Start a timer
                start_time = time.time()
                
                try:
                    # Extract paragraph text from the link with a timeout
                    text = extract_paragraph_text(url, driver, timeout=30)
                    
                    # Check if the operation took more than 10 seconds
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 10:
                        print(f"Skipped link due to timeout: {url}")
                        continue
                
                except Exception as e:
                    print(f"Error processing page {url}: {e}")
                    text = "Error loading page"
                
                # Write the title and extracted text to the new CSV file
                if "No <p> tags found" not in text and "Error loading page" not in text and "Timeout" not in text:
                    writer.writerow([title, text])

# Close the browser after processing all links
driver.quit()

print("Text extraction completed and saved to 'gnews_text2.csv'.")
