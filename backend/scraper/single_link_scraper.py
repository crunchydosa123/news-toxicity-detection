from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Function to clean the extracted text
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.strip()
    return text

# Function to extract text from <p> tags for a given URL
def extract_paragraph_text(url, driver, timeout=30):
    try:
        # Navigate to the URL
        driver.get(url)
        
        # Wait for the <p> tags to load
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, 'p'))
        )
        
        # Get all <p> tags and extract their text
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        if not paragraphs:
            return "No <p> tags found on the page."
        
        # Combine text from all paragraphs
        text = ' '.join([para.text for para in paragraphs]).strip()
        return text if text else "No text found on the page."
    
    except Exception as e:
        return f"Error: {str(e)}"

# Set up the Selenium WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run browser in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)  # Adjust path if needed
    return driver

# Flask route to handle the API call
@app.route('/extract_text', methods=['POST'])
def extract_text_api():
    # Get JSON data from the request
    data = request.json
    
    # Ensure the URL is provided
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    
    # Initialize the WebDriver
    driver = setup_driver()
    try:
        # Extract text from the given URL
        raw_text = extract_paragraph_text(url, driver)
        cleaned_text = clean_text(raw_text)
        return jsonify({'url': url, 'text': cleaned_text})
    
    finally:
        # Close the browser
        driver.quit()

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
