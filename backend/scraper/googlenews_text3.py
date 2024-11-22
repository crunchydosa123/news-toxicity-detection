from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Function to extract text from <p> tags given a URL
def extract_paragraph_text(url, driver, timeout=30):
    driver.get(url)
    wait = WebDriverWait(driver, timeout)

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        if not paragraphs:
            return {"url": url, "text": "No <p> tags found"}

        paragraph_text = ' '.join([para.text for para in paragraphs]).strip()
        return {"url": url, "text": paragraph_text} if paragraph_text else {"url": url, "text": "No text found"}

    except TimeoutException:
        return {"url": url, "text": "Timeout"}

    except Exception as e:
        return {"url": url, "text": f"Error loading page: {e}"}

def extract_text_from_articles(unique_articles):
    driver = webdriver.Chrome()
    results = []

    for article in unique_articles:
        title = article['title']
        url = article['link']

        if url:
            try:
                text = extract_paragraph_text(url, driver)
                text['title'] = title  # Add title to the result
                results.append(text)
            except Exception as e:
                results.append({"url": url, "text": f"Error processing page: {e}"})

    driver.quit()
    return results  # Return the list of extracted text data
