import pandas as pd
import numpy as np
import re
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from sklearn.preprocessing import MinMaxScaler
from multiprocessing import Pool
import torch

# Load data
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

# Load model with dynamic quantization for CPU optimization
model_name = "facebook/bart-large-mnli"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)  # Optimize for CPU

classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer, device=-1)  # Use CPU

# Define positive and negative categories
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
    results = classifier(chunks, candidate_labels, truncation=True)  # Process all chunks at once

    # Aggregate raw scores
    raw_scores = {label: 0 for label in candidate_labels}
    for result in results:
        for label, score in zip(result["labels"], result["scores"]):
            raw_scores[label] += score

    max_raw_score = max(raw_scores.values())
    if max_raw_score < raw_threshold:
        return raw_scores, None, "normal"

    # Normalize scores
    scores_list = list(raw_scores.values())
    scaler = MinMaxScaler(feature_range=(0, 1))
    normalized_scores = scaler.fit_transform(np.array(scores_list).reshape(-1, 1)).flatten()

    ordered_labels = positive_labels + negative_labels
    normalized_aggregated_scores = {label: score for label, score in zip(ordered_labels, normalized_scores)}
    max_label = max(normalized_aggregated_scores, key=normalized_aggregated_scores.get)

    return raw_scores, normalized_aggregated_scores, max_label

# Parallel processing for classification
def parallel_classification(row):
    return classify_prutl_and_negatives(row['Cleaned_Text'], raw_threshold=0.5)

# Apply the classification in parallel
with Pool() as pool:
    results = pool.map(parallel_classification, df.to_dict('records'))

# Unpack results into the DataFrame
df['Raw_Scores'], df['Aggregated_Scores'], df['Final_Attribute'] = zip(*results)

# Save results
df.to_csv('classified_prutl_articles_with_raw_scores.csv', index=False)
