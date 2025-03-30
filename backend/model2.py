import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Function to normalize profanity replacements
def normalize_word(word):
    replacements = {
        '@': 'a', '1': 'i', '!': 'i', '3': 'e', '0': 'o', '7': 't',
       r'\|\|': 'n', r'\|\\\|': 'n', r'\\': 'l', r'\(': 'c', r'\)': 'c', '5': 's'
    }
    
    # Apply replacements
    for key, val in replacements.items():
        word = re.sub(key, val, word)
    #print(f"After replacements: {word}")
    # Handle repeated characters (e.g., fuuuuck -> fuck)
    word = re.sub(r'(.)\1{2,}', r'\1', word)
    #print(f"After removing repeated characters: {word}")
    # Common misspellings
    corrections = {
        'fukc': 'fuck', 'sh1t': 'shit', 'f@ck': 'fuck', 'd@mn': 'damn'
    }
    
    return corrections.get(word, word)

# Sample dataset (Word, Severity Level)
data = [
    ("fuck", 5),
    ("shit", 5),
    ("bitch", 5),
    ("ass", 5),
    ("pussy", 5),
    ("damn", 3),
    ("crap", 3),
    ("heck", 2),
    ("darn", 2),
    ("frick", 2),
    ("dang", 2),
    ("butt", 1),
    ("poop", 1),
    ("golly", 0),
    ("gee", 0),
    ("sh1t", 5),
    ("f@ck", 5),
    ("fukc", 5),
    ("d@mn", 3),
     ("hi", 0),
    ("hello", 0),
    ("good", 0),
    ("morning", 0),
    ("friend", 0),
    ("nice", 0),
    ("love", 0),
    ("great", 0),
    ("awesome", 0),
    ("peace", 0),
    ("dick", 5)
]

# Normalize dataset
df = pd.DataFrame(data, columns=["word", "severity"])
df["normalized"] = df["word"].apply(normalize_word)

# Feature extraction using TF-IDF vectorizer
vectorizer = TfidfVectorizer(ngram_range=(1,2), analyzer='char')
X = vectorizer.fit_transform(df["normalized"])
y = df["severity"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print(classification_report(y_test, y_pred))

# Function to predict severity of new words
def predict_severity(word):
    normalized_word = normalize_word(word)
    word_vec = vectorizer.transform([normalized_word])
    severity = model.predict(word_vec)[0]
    return {"original": word, "normalized": normalized_word, "severity": severity}

# Example usage
print(predict_severity("wow!"))