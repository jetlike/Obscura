from transformers import pipeline

# Load the zero-shot classification model (used for toxicity detection)
classifier = pipeline("zero-shot-classification")

# Function to classify text as toxic or not toxic
def check_toxicity(text: str):
    # Define candidate labels (e.g., toxic or not toxic)
    candidate_labels = ["toxic", "not toxic"]
    
    # Classify the text
    result = classifier(text, candidate_labels)
    
    # Display the result
    print(f"Text: {text}")
    print(f"Prediction: {result['labels'][0]} with score: {result['scores'][0]:.4f}")
    print("=" * 50)

# Example texts to test
texts = [
    "Damn, that’s hella cool",
    "Damn, go to hell",
    "/\/!994, you are very kind."
]

# Check toxicity for each text
for text in texts:
    check_toxicity(text)
