import json
import pickle
import numpy as np
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel

# --- Configuration ---
# Define the input and output paths
INPUT_PATH = "data/ds_corpus_clean.jsonl"
OUTPUT_PATH = "data/embeddings.pkl"

# Define the model to use
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
BATCH_SIZE = 64

# --- Helper function for mean pooling ---
def mean_pooling(model_output, attention_mask):
    """
    Performs mean pooling on the token embeddings using PyTorch.    
    This function takes the raw output from the transformer model and
    averages the token embeddings, ignoring padding tokens, to create a
    single, fixed-size sentence embedding.
    """
    token_embeddings = model_output[0]  # first item of model_output contains token embeddings
    
    # Expand attention mask to match embeddings shape
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    
    # Sum embeddings, ignoring padding tokens
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    
    # Sum mask to get number of real tokens
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    # Return mean embeddings
    return sum_embeddings / sum_mask

# --- Main ---
def create_embeddings(input_path, output_path):
    """
    Reads a jsonl file, generates sentence embeddings using a Hugging Face
    transformers model in TensorFlow, and saves them.
    """
    print(f"Loading tokenizer and model: {MODEL_NAME}")
    print("This may take a while...")
    print("Please wait...")
    print("-" * 50)
    print("Starting the embedding process...")
    print("-" * 50)

    # 1. Load the tokenizer and the model from Hugging Face Hub
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    
    # Move model to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    print(f"Using device: {device}")

    # 2. Load the jsonl file
    print(f"Reading data from {input_path}...")
    doc_ids = []
    text_to_embed = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            doc_ids.append(data.get('id'))
            text_to_embed.append(data.get('text'))
    
    print(f"Found {len(text_to_embed)} documents to embed.")
    print("-" * 50)
    print("Starting the embedding process...")
    print("-" * 50)

    # --- Embedding Generation ---
    print("-" * 50)
    print(f"Generating embeddings in batches of size {BATCH_SIZE}...")
    print("This may take a while...")
    print("Please wait...")
    print("-" * 50)

    all_embeddings = []
    for i in tqdm(range(0, len(text_to_embed), BATCH_SIZE)):
        batch = text_to_embed[i:i+BATCH_SIZE]

        # 3. Tokenize the batch
        # This converts words to nums and creates attention masks
        inputs = tokenizer(batch,
         padding=True, 
         truncation=True, 
         return_tensors='pt', 
         max_length=512
         )

        # Move inputs to GPU
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # 4. Pass the tokenized inputs to the model (inference mode).
        with torch.no_grad():
            outputs = model(**inputs)

        # 5. Pool the model output to get sentence embeddings
        batch_embeddings = mean_pooling(outputs, inputs['attention_mask'])

        all_embeddings.append(batch_embeddings.cpu().numpy())

    # Combine the embeddings into a single array
    embeddings_matrix = np.vstack(all_embeddings)
    print(f"Embeddings matrix shape: {embeddings_matrix.shape}")

    # --- Saving the Output ---
    # Package all data into a single dictionary for easy loading in the next step.
    output_data = {
        'ids': doc_ids,
        'embeddings': embeddings_matrix,
        'documents': text_to_embed  # Assuming 'texts_to_embed' holds your original text
    }

    print(f"Saving packaged data to {output_path}...")

    with open(output_path, 'wb') as f_out:
        pickle.dump(output_data, f_out)
    
    print(f"Data saved to {output_path}")
    print("Done!")
    print("-" * 50)
    print("Embedding process completed successfully.")
    print("-" * 50)


if __name__ == "__main__":
    create_embeddings(INPUT_PATH, OUTPUT_PATH)
