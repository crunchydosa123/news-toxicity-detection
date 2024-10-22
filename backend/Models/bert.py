import pandas as pd
import numpy as np
import re
from transformers import pipeline
# Load the CSV file
df = pd.read_csv('./gnews_text2.csv')

# Function to clean the text
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = text.strip()
    return text

# Clean the Text column
df['Cleaned_Text'] = df['Text'].apply(clean_text)

# Initialize the sentiment analysis pipeline with a suitable model
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to classify sentiment of long text with chunking and aggregation
def classify_long_text(text):
    max_length = 512  # Define max length based on the model's capability
    chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    
    # Classify each chunk and collect the results
    results = classifier(chunks)

    # Calculate weighted averages of sentiment scores
    negative_scores = [result['score'] for result in results if result['label'] == 'NEGATIVE']
    positive_scores = [result['score'] for result in results if result['label'] == 'POSITIVE']

    # Calculate averages, if available
    avg_negative_score = np.mean(negative_scores) if negative_scores else 0
    avg_positive_score = np.mean(positive_scores) if positive_scores else 0

    # Apply a threshold to determine sentiment
    threshold = 0.5  # Define a threshold for classification
    if avg_negative_score >= threshold:
        return 'Toxic'  # Negative sentiment indicates toxicity
    else:
        return 'Non-Toxic'  # Positive sentiment indicates non-toxicity

# Apply the classification function to each cleaned text
df['Sentiment'] = df['Cleaned_Text'].apply(classify_long_text)

# Save the results to a new CSV file
df.to_csv('classified_articles.csv', index=False)
