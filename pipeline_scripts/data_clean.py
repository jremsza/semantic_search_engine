import sys
import os

# Add src directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import (
    basic_clean, 
    advanced_clean, 
    read_jsonl, 
    write_jsonl, 
    get_data_path,
    MIN_CHAR_LENGTH
)

# Configuration
# -----------------------------------------------------------------------------
INPUT_FILE = get_data_path("ds_corpus.jsonl")
OUTPUT_FILE = get_data_path("ds_corpus_clean.jsonl")

# Main Function
# -----------------------------------------------------------------------------

def main():
    """
    Main function to clean the input file and save the output to a new file.
    """
    
    # Read the input data
    data = read_jsonl(INPUT_FILE)
    if not data:
        return

    print(f"Processing {len(data)} docs...")
    processed_docs = []

    for record in data:
        title = record.get('title', '')
        text = record.get('text', '')

        text_chunks = advanced_clean(text, MIN_CHAR_LENGTH)
        
        # Create a new record for each chunk, linking back to the original article
        for i, chunk in enumerate(text_chunks):
            chunk_record = {
                "id": f"{record.get('id')}_{i}", # Create a unique ID for each chunk
                "title": title,
                "text": chunk,
                "url": record.get("url")
            }
            processed_docs.append(chunk_record)

    print(f"Successfully processed {len(processed_docs)} chunks.")

    # Write the processed chunks to a new .jsonl file.
    print(f"\nWriting {len(processed_docs)} processed chunks to '{OUTPUT_FILE}'...")
    if write_jsonl(processed_docs, OUTPUT_FILE):
        print("SUCCESS: Data cleaning and chunking complete.")
    else:
        print("ERROR: Could not write to file.")

if __name__ == "__main__":
    main()