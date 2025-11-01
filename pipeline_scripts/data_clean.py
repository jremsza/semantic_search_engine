import sys
import os
import re
import unicodedata

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

# Normalization helpers (one-off dash/encoding fix)
# -----------------------------------------------------------------------------
_DASH_RX = re.compile(r"[‐‑‒–—―−]")  # common dash/minus variants

def normalize_text(value: str) -> str:
    """Normalize unicode text to stabilize IDs/titles across sources.

    - NFKC normalization
    - Map all dash/minus variants to ASCII '-'
    - Replace non-breaking space with regular space
    - Drop the Unicode replacement character if present
    """
    if value is None:
        return ""
    text = unicodedata.normalize("NFKC", str(value))
    text = _DASH_RX.sub("-", text)
    text = text.replace("\u00A0", " ")
    text = text.replace("�", "")
    return text.strip()

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
        # Normalize inputs (IDs, titles, text) to fix dash/encoding inconsistencies
        base_id = normalize_text(record.get('id', ''))
        title = normalize_text(record.get('title', ''))
        text = normalize_text(record.get('text', ''))

        text_chunks = advanced_clean(text, MIN_CHAR_LENGTH)
        
        # Create a new record for each chunk, linking back to the original article
        for i, chunk in enumerate(text_chunks):
            # Also normalize chunk output to ensure consistency end-to-end
            chunk = normalize_text(chunk)
            chunk_record = {
                "id": f"{base_id}_{i}", # Create a unique ID for each chunk
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