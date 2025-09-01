# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from analyzer import analyze_ccn

# Define the data model for the incoming request
class CCNRequest(BaseModel):
    note_text: str

app = FastAPI(
    title="RiskON 2025 CCN Analyzer",
    description="An API to enhance the quality of Client Contact Notes using AI.",
)

@app.post("/analyze/")
def analyze_note(request: CCNRequest) -> dict:
    """
    Accepts a CCN text and returns a quality analysis.
    """
    analysis_result = analyze_ccn(request.note_text)
    return analysis_result