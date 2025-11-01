"""
Utility functions for the semantic search project.
Contains shared functions for text processing, embeddings, and file I/O.
"""

import json
import os
import re
import pickle
import numpy as np
from typing import List, Dict, Any, Union


# =============================================================================
# TEXT CLEANING FUNCTIONS
# =============================================================================

def basic_clean(text: str) -> str:
    """
    Performs basic cleaning on Wikipedia text.
    
    Args:
        text: Raw Wikipedia text
        
    Returns:
        Basic cleaned text
    """
    # Remove citation numbers like [1], [2], etc.
    text = re.sub(r'\[\d+\]', '', text)
    
    # Clean up multiple newlines
    text = re.sub(r'\n+', '\n', text)
    
    return text.strip()


def advanced_clean(text: str, min_char_length: int = 125) -> List[str]:
    """
    Cleans Wikipedia text and splits it into meaningful paragraph chunks.
    
    Args:
        text: The raw text content of a Wikipedia article
        min_char_length: Minimum character length for chunks
        
    Returns:
        A list of cleaned text chunks
    """
    # First apply basic cleaning
    text = basic_clean(text)
    
    # Remove headers
    text = re.sub(r'==.?==+', '', text)

    # Remove extra lines
    text = re.sub(r'\n{2,}', '\n', text)

    # Split into chunks
    chunks = text.split('\n')

    # Filter for chunks with minimum length
    final_chunks = [
        chunk.strip() for chunk in chunks 
        if len(chunk.strip()) >= min_char_length
    ]

    return final_chunks


# =============================================================================
# FILE I/O FUNCTIONS
# =============================================================================

def read_jsonl(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads a JSONL file and returns a list of dictionaries.
    
    Args:
        file_path: Path to the JSONL file
        
    Returns:
        List of dictionaries from the JSONL file
    """
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return data


def write_jsonl(data: List[Dict[str, Any]], file_path: str) -> bool:
    """
    Writes a list of dictionaries to a JSONL file.
    
    Args:
        data: List of dictionaries to write
        file_path: Path to the output JSONL file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for record in data:
                f.write(json.dumps(record) + '\n')
        return True
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        return False


# =============================================================================
# PATH UTILITIES
# =============================================================================

def ensure_dir(directory: str) -> None:
    """
    Creates a directory if it doesn't exist.
    
    Args:
        directory: Directory path to create
    """
    os.makedirs(directory, exist_ok=True)


def get_data_path(filename: str) -> str:
    """
    Gets the full path for a file in the data directory.
    Automatically detects project root by looking for this file (utils.py)
    to work regardless of current working directory.
    
    Args:
        filename: Name of the file
        
    Returns:
        Full absolute path to the file
    """
    # Get the directory where this utils.py file is located (src/)
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root
    project_root = os.path.dirname(utils_dir)
    # Return absolute path to data/filename
    return os.path.join(project_root, "data", filename)


# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

# Model configuration
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
BATCH_SIZE = 64
EMBEDDING_DIMENSION = 384

# File paths
RAW_DATA_FILE = "ds_corpus.jsonl"
CLEAN_DATA_FILE = "ds_corpus_clean.jsonl"
EMBEDDINGS_FILE = "models/embeddings.pkl"

# Text processing
MIN_CHAR_LENGTH = 150
