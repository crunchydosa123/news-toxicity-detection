import pandas as pd
import numpy as np
import re
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
import joblib

train_data = pd.read_csv('train.csv')  
test_data = pd.read_csv('test.csv')   


nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r'\\n', ' ', text)
    text = re.sub(r'[^\\w\\s]', '', text.lower())  
    return text


train_data['clean_comment'] = train_data['comment_text'].apply(clean_text)
test_data['clean_comment'] = test_data['comment_text'].apply(clean_text)

X = train_data['clean_comment']
y = train_data[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']]

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

tfidf_vectorizer = TfidfVectorizer(max_features=10000) 
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_val_tfidf = tfidf_vectorizer.transform(X_val)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_tfidf, y_train)
rf_predictions = rf_model.predict(X_val_tfidf)

print("Random Forest Classification Report")
print(classification_report(y_val, rf_predictions))


joblib.dump(rf_model, 'rf_model.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')

chunk_size = 300  

def chunk_text(text, chunk_size):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


tokenizer = Tokenizer()  
tokenizer.fit_on_texts(X_train)

X_train_chunks = []
y_train_chunks = []
for i in range(len(X_train)):
    chunks = chunk_text(X_train.iloc[i], chunk_size)
    X_train_chunks.extend(chunks)
    y_train_chunks.extend([y_train.iloc[i].values] * len(chunks)) 

X_train_seq = tokenizer.texts_to_sequences(X_train_chunks)
X_val_chunks = []
for i in range(len(X_val)):
    chunks = chunk_text(X_val.iloc[i], chunk_size)
    X_val_chunks.extend(chunks)

X_val_seq = tokenizer.texts_to_sequences(X_val_chunks)

X_train_pad = pad_sequences(X_train_seq) 
X_val_pad = pad_sequences(X_val_seq)

lstm_model = Sequential()
lstm_model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=100))
lstm_model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
lstm_model.add(Dense(50, activation='relu'))
lstm_model.add(Dropout(0.5))
lstm_model.add(Dense(6, activation='sigmoid'))

lstm_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
lstm_model.fit(X_train_pad, np.array(y_train_chunks), epochs=3, batch_size=64, validation_split=0.1)

lstm_predictions = lstm_model.predict(X_val_pad)
lstm_predictions = (lstm_predictions > 0.5).astype(int)

print("LSTM Classification Report")
print(classification_report(y_val, lstm_predictions))

lstm_model.save('lstm_model.h5')

bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=6)

def encode_bert_texts(texts, max_len=512):
    encoded_texts = []
    attention_masks = []
    for text in texts:
        tokenized_text = bert_tokenizer.encode_plus(text, 
                                                     max_length=max_len, 
                                                     padding='max_length', 
                                                     truncation=True, 
                                                     return_tensors='tf')
        encoded_texts.append(tokenized_text['input_ids'])
        attention_masks.append(tokenized_text['attention_mask'])
    return np.array(encoded_texts), np.array(attention_masks)

X_val_bert_chunks, attention_masks_val = encode_bert_texts(X_val)

bert_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=2e-5), loss='binary_crossentropy', metrics=['accuracy'])
bert_model.fit([X_val_bert_chunks, attention_masks_val], y_val, epochs=2, batch_size=16)

bert_predictions = bert_model.predict([X_val_bert_chunks, attention_masks_val]).logits
bert_predictions = tf.sigmoid(bert_predictions).numpy()
bert_predictions = (bert_predictions > 0.5).astype(int)

print("BERT Classification Report")
print(classification_report(y_val, bert_predictions))

bert_model.save('bert_model.h5')


ensemble_predictions = (rf_predictions + lstm_predictions + bert_predictions) / 3
ensemble_predictions = (ensemble_predictions > 0.5).astype(int)

print("Ensemble Classification Report")
print(classification_report(y_val, ensemble_predictions))

X_test_tfidf = tfidf_vectorizer.transform(test_data['clean_comment'])
X_test_seq = tokenizer.texts_to_sequences(test_data['clean_comment'])
X_test_pad = pad_sequences(X_test_seq)

rf_test_predictions = rf_model.predict(X_test_tfidf)

X_test_chunks = []
for i in range(len(test_data)):
    chunks = chunk_text(test_data['clean_comment'].iloc[i], chunk_size)
    X_test_chunks.extend(chunks)


X_test_seq = tokenizer.texts_to_sequences(X_test_chunks)

X_test_pad = pad_sequences(X_test_seq)

lstm_test_predictions = lstm_model.predict(X_test_pad)
lstm_test_predictions = (lstm_test_predictions > 0.5).astype(int)

X_test_bert_chunks, attention_masks_test = encode_bert_texts(test_data['clean_comment'])
bert_test_predictions = bert_model.predict([X_test_bert_chunks, attention_masks_test]).logits
bert_test_predictions = tf.sigmoid(bert_test_predictions).numpy()
bert_test_predictions = (bert_test_predictions > 0.5).astype(int)


ensemble_test_predictions = (rf_test_predictions + lstm_test_predictions + bert_test_predictions) / 3
ensemble_test_predictions = (ensemble_test_predictions > 0.5).astype(int)

results_df = pd.DataFrame({
    'comment_text': test_data['comment_text'],
    'toxic': ensemble_test_predictions[:, 0],
    'severe_toxic': ensemble_test_predictions[:, 1],
    'obscene': ensemble_test_predictions[:, 2],
    'threat': ensemble_test_predictions[:, 3],
    'insult': ensemble_test_predictions[:, 4],
    'identity_hate': ensemble_test_predictions[:, 5],
})


results_df.to_csv('predictions.csv', index=False)
print("Predictions saved to predictions.csv")