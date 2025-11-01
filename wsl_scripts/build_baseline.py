import os
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# --- Configuration ---
INPUT_PATH = "data/ds_corpus_clean.jsonl"
OUTPUT_PATH = "models/tfidf_baseline.joblib"

corpus = []
ids = []

with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        corpus.append(data['text'])
        ids.append(data['id'])

print(f"Loaded {len(corpus)} documents.")

print("-" * 60)
print("Building TF-IDF baseline model...")
print("-" * 60)

# --- Creat and fit the vectorizer ---
vectorizer = TfidfVectorizer(stop_words='english')
print("Fitting the vectorizer...")

print("-" * 60)
tfidf_matrix = vectorizer.fit_transform(corpus)
print("Vectorizer fitted successfully.")
print(f"Matrix shape: {tfidf_matrix.shape}")
print("-" * 60)

# --- Save the vectorizer ---
# Save three things:
# 1. The 'vectorizer' (so we can transform new queries the same way)
# 2. The 'tfidf_matrix' (the "index" of all our documents)
# 3. The 'ids' (to map the matrix rows back to our document IDs)

MODEL_DIR = 'models'
os.makedirs(MODEL_DIR, exist_ok=True) # Create the directory if it doesn't exist

joblib.dump(vectorizer, os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib"))
joblib.dump(tfidf_matrix, os.path.join(MODEL_DIR, "tfidf_matrix.joblib"))
joblib.dump(ids, os.path.join(MODEL_DIR, "tfidf_ids.joblib"))

print(f"Baseline model components saved to '{MODEL_DIR}' directory.")
print("Baseline build complete.")
print("-" * 60)