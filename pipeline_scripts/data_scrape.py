import wikipediaapi
import os
import time
import json

# Configuration
# -----------------------------------------------------------------------------
TOPICS = [
    "Artificial intelligence", "Machine learning", "Data science", "Deep learning", "Artificial Neural Network", "Feature learning",
    "Convolutional Neural Network", "Recurrent Neural Network", "LSTM", "Gated recurrent unit", "Transformer (deep learning architecture)", "Rectified linear unit",
    "Attention mechanism", "Generative Adversarial Network", "Autoencoder", "Neural network", "Supervised learning", "Unsupervised learning", 
    "Reinforcement learning", "Linear programming", "Integer programming", "Linear regression", "Logistic regression", "Support vector machine", 
    "Decision tree", "Markov chain", "Random forest", "Gradient boosting", "K-means clustering", "Principal component analysis", "Dimensionality reduction", "TSNE", 
    "Natural language processing", "Computer vision", "Overfitting", "Cross-validation (statistics)", "Partial least squares", "Confusion matrix", "Bootstrapping (statistics)",
    "Precision and recall", "Accuracy and precision", "Receiver operating characteristic", "Data engineering", "Latent Dirichlet allocation", "Out-of-bag error", "Naive Bayes classifier",
    "Bias-variance tradeoff", "Hyperparameter tuning", "Feature engineering", "Data mining", "Data visualization", "Singular value decomposition", "Eigenvalues", "Eigenvectors",
    "Big data", "TensorFlow", "Scikit-learn", "Pandas (software)", "NumPy", "R (programming language)", "Python (programming language)", "Z-score", "Word embedding",
    "Lasso regression", "Ridge regression", "Elastic net regression", "XGBoost", "AdaBoost", "Bootstrap aggregating", "Confidence interval", "p-value", "Statistical hypothesis test",
    "Boosting", "Ensemble learning", "Model evaluation", "F-test", "Student's t-test", "ANOVA", "Chi-square test", "Central limit theorem", "Boosting (machine learning)",
    "Gradient descent", "Root mean square deviation", "Collinearity", "Multicollinearity", "Bayes' theorem", "Data wrangling", "Graph database", "Snowflake schema",
    "Mean absolute percentage error", "Coefficient of determination", "Akaike information criterion", "Bayesian information criterion", "Cross-entropy", "Hierarchical clustering", "DBSCAN",
    "Mean squared error", "Mean absolute error", "SQL", "NoSQL", "Database", "Relational database", "Key-value store", "Document-oriented database", "Vector database",
    "Data warehouse", "Data lake", "Data pipeline", "Data mart", "Online analytical processing", "Online transaction processing", "Extract, transform, load", "Stemming",
    "tf–idf", "Word2vec", "GloVe", "BERT (language model)", "Generative pre-trained transformer", "XLNet","Lemmatization", "Large language model", "Knowledge graph embedding", "Topic models",
    "Knowledge graph", "Named-entity recognition", "Bag-of-words model", "Part-of-speech tagging", "Dijkstra's algorithm"
    ]
# Output directory and filename.
OUTPUT_DIR = "data"
OUTPUT_FILENAME = "ds_corpus.jsonl"

# Initialize the Wikipedia API.
wiki_api = wikipediaapi.Wikipedia(
    user_agent='msds-498_Project/1.0 (jremsza2@gmail.com)',
    language='en'
)

# Main Function
# -----------------------------------------------------------------------------
def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    corpus = []
    for i, topic in enumerate(TOPICS):
        print(f"Processing {topic}... ({i+1}/{len(TOPICS)})")

        try:
            page = wiki_api.page(topic)
        except Exception as e:
            print(f"Error fetching {topic}: {e}")
            continue

        # Create a dictionary for the each article.
        article = {
            "id": topic.replace(" ", "_"),
            "url": page.canonicalurl,
            "title": page.title,
            "text": page.text  # Raw text - no cleaning
        }
        corpus.append(article)

        time.sleep(5)

    # Check if any articles were found
    if not corpus:
        print("No articles found.")
        return

    # Write to json file
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for article in corpus:
                f.write(json.dumps(article) + '\n')
        print(f"Successfully wrote to {output_path}")
        print("Data scraping complete.")
    except Exception as e:
        print(f"Error writing to {output_path}: {e}")

if __name__ == "__main__":
    main()
