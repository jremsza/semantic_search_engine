import json
import pickle
import numpy as np
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModel
from tqdm import tqdm


# --- Configuration ---
# Define the inout and output paths
input_path = "data/ds_corpus_clean.jsonl"
output_path = "data/embeddings.pkl"

# Define the model to use
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
BATCH_SIZE = 64

# --- Helper function for mean pooling ---
def mean_pooling(model_output, attention_mask):
    """
    Performs mean pooling on the token embeddings.
    
    This function takes the raw output from the transformer model and
    averages the token embeddings, ignoring padding tokens, to create a
    single, fixed-size sentence embedding.
    """

    token_embeddings = model_output[0] # first item of model_output contains token embeddings
    input_mask_expanded = tf.cast(
        tf.broadcast_to(tf.expand_dims(attention_mask, axis=-1), tf.shape(token_embeddings)),
        dtype=tf.float32
    )

    
   





