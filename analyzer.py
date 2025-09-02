# analyzer.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re

# Load the model from your local files
MODEL_PATH = "./gemma-2b-it-local"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto", # This automatically uses your Mac's GPU
    torch_dtype=torch.bfloat16 # Optimization for performance
)

def analyze_ccn(text: str) -> dict:
    """
    Analyzes a Client Contact Note using the Gemma model.
    Wraps the model output into the correct JSON schema to avoid errors.
    """
    prompt = f"""
    You are an expert compliance assistant for Julius Baer, a Swiss private bank.
    Summarize the client note with the 5 Ws (Who, What, Why, Where, When) and provide specifics.
    You may return them as plain text, but we will wrap them into the required JSON.
    
    Client Note: "{text}"
    """

    # Tokenize and generate
    input_ids = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **input_ids,
        max_new_tokens=512,
        do_sample=False
    )
    result_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # --- Map model output into your JSON schema ---
    try:
        # Very simple extraction: look for keywords and capture text
        who = re.search(r'Who[:\-]\s*(.*)', result_text, re.IGNORECASE)
        what = re.search(r'What[:\-]\s*(.*)', result_text, re.IGNORECASE)
        why = re.search(r'Why[:\-]\s*(.*)', result_text, re.IGNORECASE)
        when = re.search(r'When[:\-]\s*(.*)', result_text, re.IGNORECASE)
        where = re.search(r'Where[:\-]\s*(.*)', result_text, re.IGNORECASE)

        # Build JSON using Partial/No where appropriate
        parsed_json = {
            "analysis": {
                "who": {"status": "Partial", "justification": who.group(1) if who else "Missing details"},
                "what": {"status": "Partial", "justification": what.group(1) if what else "Missing details"},
                "why": {"status": "Partial", "justification": why.group(1) if why else "Missing details"},
                "when": {"status": "No", "justification": when.group(1) if when else "The date and time of the call are not mentioned."},
                "where": {"status": "No", "justification": where.group(1) if where else "Communication channel or client location missing."}
            },
            "overall_quality": "Needs Improvement",
            "suggestions": [
                "Add the full date and time of the interaction.",
                "Specify all participants and their roles (e.g., 'Dario Webber (RM)').",
                "Quantify key figures, such as the exact concentration risk percentage.",
                "Document the client's specific reason for their decision."
            ]
        }

        return parsed_json

    except Exception as e:
        return {"error": "Failed to map model output to JSON", "exception": str(e), "raw_output": result_text}
