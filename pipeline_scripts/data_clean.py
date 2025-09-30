import json
import os
import re


# Configuration
# -----------------------------------------------------------------------------

# Input file 
INPUT_FILE = os.path.join("data", "ds_corpus.jsonl")

# Output file 
OUTPUT_FILE = os.path.join("data", "ds_corpus_clean.jsonl")

# Set min char length
MIN_CHAR_LENGTH = 125

# Advanced cleaning parameters
# -----------------------------------------------------------------------------
def advanced_clean(text: str) -> list[str]:
    """
    Cleans Wikipedia text and splits it into meaningful paragraph chunks.
    
    Args:
        text: The raw text content of a Wikipedia article.
        
    Returns:
        A list of cleaned text chunks.
    """
    # Remove headers
    text = re.sub(r'==.?==+', '', text)

    # Remove extra lines
    text = re.sub(r'\n{2,}', '\n', text)

    # Split into chunks
    chunks = text.split('\n')

    # Filter for chunks with minimum length
    final_chunks = [
        chunk.strip() for chunk in chunks 
        if len(chunk.strip()) >= MIN_CHAR_LENGTH
    ]

    return final_chunks

# Main Function
# -----------------------------------------------------------------------------

def main():
    """
    Main function to clean the input file and save the output to a new file.
    """
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    except FileNotFoundError:
        print(f"Error: Input file {INPUT_FILE} not found.")
        return

    print(f"Processing {len(lines)} docs...")
    processed_docs = []

    for line in lines:
        data = json.loads(line)
        title = data.get('title', '')
        text = data.get('text', '')

        text_chunks = advanced_clean(text)
        
        # Create a new record for each chunk, linking back to the original article
        for i, chunk in enumerate(text_chunks):
            chunk_record = {
                "id": f"{data.get('id')}_{i}", # Create a unique ID for each chunk
                "title": title,
                "text": chunk,
                "url": data.get("url")
            }
            processed_docs.append(chunk_record)

    print(f"Successfully processed {len(processed_docs)} chunks.")

    # Write the processed chunks to a new .jsonl file.
    print(f"\nWriting {len(processed_docs)} processed chunks to '{OUTPUT_FILE}'...")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for record in processed_docs:
                f.write(json.dumps(record) + '\n')
        print("SUCCESS: Data cleaning and chunking complete.")
    except Exception as e:
        print(f"ERROR: Could not write to file. Reason: {e}")

if __name__ == "__main__":
    main()