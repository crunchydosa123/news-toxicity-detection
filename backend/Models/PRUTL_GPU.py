import pandas as pd
import numpy as np
import re
from transformers import pipeline
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('gnews_text2.csv')

# Function to clean the text
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) 
    text = re.sub(r'<.*?>', '', text)  
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  
    text = text.strip()
    return text

# Clean the Text column
df['Cleaned_Text'] = df['Text'].apply(clean_text)

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", device=0)  

# Define the positive and negative categories
positive_labels = ["peace", "respect", "unity", "trust", "justice"]
negative_labels = ["conflict", "disrespect", "chaos", "mistrust", "injustice"]
candidate_labels = positive_labels + negative_labels

# Sliding window method
def sliding_window(text, window_size=512, overlap=50):
    text_length = len(text)
    chunks = [text[i:i + window_size] for i in range(0, text_length, window_size - overlap)]
    return chunks

# Classification function
def classify_prutl_and_negatives(text, raw_threshold=0.5):
    chunks = sliding_window(text)
    results = classifier(chunks, candidate_labels)

    raw_scores = {label: 0 for label in candidate_labels}
    for result in results:
        for label, score in zip(result["labels"], result["scores"]):
            raw_scores[label] += score

    max_raw_score = max(raw_scores.values())
    #print(f"Raw Scores: {raw_scores}, Max Raw Score: {max_raw_score}, Threshold: {raw_threshold}")

    if max_raw_score < raw_threshold:
        #print("Classified as 'normal'")
        return raw_scores, None, "normal"

    scores_list = list(raw_scores.values())
    scaler = MinMaxScaler(feature_range=(0, 1))
    normalized_scores = scaler.fit_transform(np.array(scores_list).reshape(-1, 1)).flatten()

    ordered_labels = positive_labels + negative_labels
    normalized_aggregated_scores = {label: score for label, score in zip(ordered_labels, normalized_scores)}
    max_label = max(normalized_aggregated_scores, key=normalized_aggregated_scores.get)

    return raw_scores, normalized_aggregated_scores, max_label

# Apply the classification function
df['Raw_Scores'], df['Aggregated_Scores'], df['Final_Attribute'] = zip(*df['Cleaned_Text'].apply(
    lambda text: classify_prutl_and_negatives(text, raw_threshold=0.5)
))

# Save results
df.to_csv('classified_prutl_articles_with_raw_scores.csv', index=False)