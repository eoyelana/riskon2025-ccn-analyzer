# analyzer.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load the model from your local files
MODEL_PATH = "./gemma-2b-it-local"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH, device_map="auto" # This automatically uses your Mac's GPU
)

def analyze_ccn(text: str) -> dict:
    """
    Analyzes a Client Contact Note using the Gemma model.
    """
    # This is where your prompt engineering will go!
    prompt = f"""
    Analyze the following client note. Based *only* on the text provided, evaluate if each of the 5 Ws is present. For each W, provide a 'status' (Yes, No, or Partial) and a brief 'justification'.

    Client Note: "{text}"

    Return your analysis as a JSON object:
    """
    
    input_ids = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**input_ids, max_new_tokens=250)
    result_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # For now, we'll just return a placeholder. You'll parse the LLM's JSON output here.
    print(result_text) # Print the raw output for now to help with debugging
    
    return {"status": "analysis_pending", "raw_output": result_text}