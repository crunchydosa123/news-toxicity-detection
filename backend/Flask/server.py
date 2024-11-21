from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import sys
import os
import importlib.util

# Add the scraper directory to the system path
sys.path.append(os.path.abspath('../scraper'))

# Load the modules from file
def load_module(module_name, module_path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

googlenews = load_module("googlenews1", os.path.join(os.path.abspath('../scraper'), 'googlenews1.py'))
removeduplicates = load_module("removeduplicates2", os.path.join(os.path.abspath('../scraper'), 'removeduplicates2.py'))
googlenews_text = load_module("googlenews_text3", os.path.join(os.path.abspath('../scraper'), 'googlenews_text3.py'))
bert_model = load_module("bert2", os.path.join(os.path.abspath('../Models'), 'bert2.py'))  # Replace with actual filename if needed

extract_and_write_links = googlenews.extract_and_write_links
remove_duplicates = removeduplicates.remove_duplicates
extract_text_from_articles = googlenews_text.extract_text_from_articles
analyze_sentiment = bert_model.analyze_sentiment  # Import the analyze sentiment function

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route('/scrape', methods=['GET'])
def scrape_articles():
    # Get keywords from the request arguments
    keywords = request.args.getlist('keywords[]')
    
    if not keywords:
        return jsonify({'error': 'No keywords provided'}), 400

    # Call the function to extract articles
    articles = extract_and_write_links(keywords)
    
    # Format the articles into a response-friendly structure
    response_data = [{'title': article[0], 'link': article[1]} for article in articles]

    # Remove duplicates from the response data
    unique_articles = remove_duplicates(response_data)

    # Extract text from unique articles
    text_data = extract_text_from_articles(unique_articles)

    return jsonify(text_data)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment_route():
    # Get the text data from the request body
    text_data = request.json  # Expecting a JSON body with the articles

    if not text_data:
        return jsonify({'error': 'No text data provided'}), 400

    # Analyze sentiment
    results = analyze_sentiment(text_data)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
