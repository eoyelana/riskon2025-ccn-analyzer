# download_model.py
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Define the model and the local directory to save it to
MODEL_NAME = "google/gemma-2b-it"
LOCAL_MODEL_PATH = "./gemma-2b-it-local"

def download_model():
    """
    Downloads the specified Hugging Face model and tokenizer and saves them
    to a local directory for offline use.
    """
    if os.path.exists(LOCAL_MODEL_PATH):
        print(f"✅ Model directory '{LOCAL_MODEL_PATH}' already exists. Skipping download.")
        return

    print(f"Downloading model and tokenizer for '{MODEL_NAME}'...")
    print("This may take a few minutes and require several gigabytes of space.")

    try:
        # Download and cache the model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

        print("Download complete. Saving to local directory...")

        # Save them to the specified local directory
        model.save_pretrained(LOCAL_MODEL_PATH)
        tokenizer.save_pretrained(LOCAL_MODEL_PATH)

        print(f"✅ Model and tokenizer saved successfully to '{LOCAL_MODEL_PATH}'.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    download_model()