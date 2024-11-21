import re
import numpy as np
from transformers import pipeline
from sklearn.preprocessing import MinMaxScaler
import json

# Function to clean the text
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.strip()
    return text

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)

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
    # Clean the input text
    cleaned_text = clean_text(text)

    # Split the text into chunks
    chunks = sliding_window(cleaned_text)

    # Perform classification on each chunk
    results = classifier(chunks, candidate_labels)

    # Aggregate raw scores
    raw_scores = {label: 0 for label in candidate_labels}
    for result in results:
        for label, score in zip(result["labels"], result["scores"]):
            raw_scores[label] += score

    # Find the maximum raw score
    max_raw_score = max(raw_scores.values())

    # Check if below the threshold
    if max_raw_score < raw_threshold:
        return raw_scores, None, "normal"

    # Normalize scores using MinMaxScaler
    scores_list = list(raw_scores.values())
    scaler = MinMaxScaler(feature_range=(0, 1))
    normalized_scores = scaler.fit_transform(np.array(scores_list).reshape(-1, 1)).flatten()

    # Map normalized scores back to labels
    ordered_labels = positive_labels + negative_labels
    normalized_aggregated_scores = {label: score for label, score in zip(ordered_labels, normalized_scores)}

    # Determine the label with the highest score
    max_label = max(normalized_aggregated_scores, key=normalized_aggregated_scores.get)

    return raw_scores, normalized_aggregated_scores, max_label

# Function to classify a single text input and return JSON output
def classify_text_as_json(text):
    # Perform classification
    raw_scores, aggregated_scores, final_attribute = classify_prutl_and_negatives(text)

    # Prepare JSON output
    output = {
        "Raw_Scores": raw_scores,
        "Aggregated_Scores": aggregated_scores,
        "Final_Attribute": final_attribute
    }

    return json.dumps(output,indent=4)

# Example Usage
input_text = """
Published - November 18, 2024 08:30 am IST Suspended IAS officer N. Prasanth addresses the media, in Trivandrum, Kerala, on November 12. | Photo Credit: PTI The story so far:Kerala has suspended two IAS officers, N. Prashant and K. Gopalakrishnan, citing violation of service rules. The charge against N. Prashant is that he had made    derogatory statements    on social media against A. Jayathilak IAS, Additional Chief Secretary, that amounted to grave indiscipline and undermining the public image of the administrative machinery of the State. The government order stated that these remarks were    unbecoming of an officer    borne in the Indian Administrative Service (IAS). Mr. Prashant alleged that Jayathilak had orchestrated baseless news reports against him. He refuted these allegations. K. Gopalakrishnan has been suspended for allegedly creating a religion-based WhatsApp group        Mallu Hindu Officers        that sowed disunity and created communal formations within the IAS cadre. He had claimed that this group was created after his mobile phone was hacked. However, the suspension order stated that the police inquiry found no evidence of such hacking and that the officer had done a    factory reset    of the phone before handing it over to police. Also read: Reining in civil servants in Kerala  The All-India Services (Conduct) Rules, 1968 (AIS rules) governs the conduct of IAS, IPS and Indian Forest Service officers. The AIS rules provide a code of conduct for the officers. Some of the rules relevant for the current issue are briefly summarised here. Officers should maintain high standards of ethics, integrity, honesty, political neutrality, accountability and transparency. They should uphold the supremacy of constitutional values. They can participate or contribute in public media in the bonafide discharge of their duties. They shall not in any communication over any public media adversely criticise the policies of the government. They shall not have recourse to any court or press for the vindication of official act, that has been subject matter of criticism, without the previous sanction of the government. It also contains an omnibus rule that the officers shall do nothing which is    unbecoming of a member of the service.    There are certain overall issues that need to be addressed. First, the rules don   t have explicit guidelines with respect to communication through social media. Second, the rules have been amended from time to time by including various new conduct guidelines that regulate both the private and official life of officers. The term    unbecoming of a member of the service    however continues as an omnibus rider that can be misused/misinterpreted. It must also be borne in mind that invariably in all cases, it is the senior officers and government who enforce these rules against junior officers and hence the latter need to be protected from any such misuse. Firstly, specific rules may be added with respect to the use of social media. This may include guidelines for the nature of official content that can be posted as well the right to defend against any defamatory campaign concerning official work. Secondly, an illustrative list may be provided for the term    unbecoming of a member of the service,    based on past instances where action had been taken on this basis. Officers, especially youngsters, should remember that anonymity is an important trait of civil servants. In the present day and age, social media is a powerful medium for providing publicity to various governmental initiatives. It educates citizens when used judiciously. However, officers should exercise responsible anonymity while discharging their functions and disseminating information about the same. Rangarajan. R is a former IAS officer and author of    Polity Simplified   . Views expressed are personal. Published - November 18, 2024 08:30 am IST Text and Context / public officials / The Hindu Explains / Kerala Copyright   2024, THG PUBLISHING PVT LTD. or its affiliated companies. All rights reserved. BACK TO TOP
"""

# Get JSON output
result_json = classify_text_as_json(input_text)

# Print JSON result
print(result_json)
