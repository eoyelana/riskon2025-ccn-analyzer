# RiskON 2025: AI-Powered Client Contact Note Analyzer

A proof-of-concept solution for the **Julius Baer RiskON 2025 Challenge**. This project leverages a local, open-source Large Language Model (LLM) to provide real-time quality assurance for manually created Client Contact Notes (CCNs).

![AI Contact Note Analyzer Banner](./assets/licensed-image.jpeg)

## 1. Challenge Overview

The core challenge is to improve the **completeness and quality** of manually entered Client Contact Notes. High-quality CCNs are critical for regulatory adherence, documenting client interactions, and proving reverse solicitation.

**Key Pain Points Addressed:**
* **Incompleteness:** Notes often miss one of the "5 Ws" (Who, What, Why, Where, When).
* **Lack of Quality:** The "What" and "Why" sections are frequently too generic, lacking the specific context needed for a robust audit trail.
* **Manual Controls:** Manual checks are resource-intensive and not scalable.

Our solution introduces an AI assistant at the point of entry to help Relationship Managers write "first time right" documentation.

## 2. Our Solution

We have developed a lightweight, secure API that analyzes a CCN and returns a structured quality assessment in real-time. A Relationship Manager can use this feedback to enhance their note before submission, directly within their existing workflow.

### Key Features
* **5 Ws Completeness Check:** Systematically verifies the presence of all five required components.
* **Quality Assessment:** Evaluates the depth and clarity of the note, providing actionable suggestions.
* **API-First Design:** Built with FastAPI for easy integration into any front-end or CRM system.
* **Secure & Offline:** Runs **100% locally** using the open-source Gemma LLM. No client data ever leaves the bank's infrastructure.
* **Developer Friendly:** Adheres to modern coding standards, including `black` formatting and `ruff` linting.

## 3. Tech Stack

This project is built entirely on open-source components that are approved for commercial use, meeting all technical requirements of the challenge.

| Component      | Technology                               | Purpose                                      |
| -------------- | ---------------------------------------- | -------------------------------------------- |
| **Language** | Python 3.9+                              | Core application logic.                      |
| **AI / LLM** | Google Gemma 2B-IT                       | Natural Language Processing & Analysis.      |
| **AI Framework** | Hugging Face `transformers` & `accelerate` | To run the LLM efficiently on local hardware. |
| **API Framework**| FastAPI                                  | To expose the analysis logic as a REST API.  |
| **Server** | Uvicorn                                  | High-performance ASGI server.                |
| **Container** | Docker                                   | For packaging the app for K8s deployment.    |
| **Code Quality** | Black, Ruff                              | Linting and code formatting.                 |
| **Testing** | Pytest                                   | For writing unit and integration tests.      |

## 4. Getting Started

Follow these instructions to set up and run the project locally on your machine.

### Prerequisites
* Git
* Python 3.9 or higher
* An active internet connection (for the initial setup and model download only).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/eoyelana/riskon2025-ccn-analyzer.git
    cd riskon2025-ccn-analyzer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download the LLM (One-time step):**
    This script downloads the Gemma model from Hugging Face and saves it locally. This requires ~5GB of disk space.
    ```bash
    python download_model.py
    ```

### Running the API

1.  **Start the local server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will now be available at `http://127.0.0.1:8000`.

2.  **Access the auto-generated documentation:**
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to see the interactive Swagger UI.

## 5. API Usage Example

You can send a `POST` request to the `/analyze/` endpoint with your note text.

**Example using `curl`:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/analyze/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "note_text": "Called Sabrina as requested by Mr Martin. We discussed the portfolio. She is fine with the concentration risk in Nvidia for now."
}'

```

The API will return a JSON object with the analysis, highlighting missing details and suggesting improvements.

```json
{
  "analysis": {
    "who": {
      "status": "Partial",
      "justification": "Mentions 'Sabrina' and 'Mr Martin', but does not include full names or roles (e.g., AH, POA) or the RM's name."
    },
    "what": {
      "status": "Partial",
      "justification": "Mentions discussing the portfolio and a concentration risk in Nvidia, but lacks specifics like the percentage of exposure."
    },
    "why": {
      "status": "Partial",
      "justification": "States Sabrina is 'fine for now' but does not capture her explicit rationale for accepting the risk."
    },
    "when": {
      "status": "No",
      "justification": "The date and time of the call are not mentioned in the note."
    },
    "where": {
      "status": "No",
      "justification": "The note does not specify the communication channel (e.g., Telephone) or the location of the client (e.g., Spain)."
    }
  },
  "overall_quality": "Needs Improvement",
  "suggestions": [
    "Add the full date and time of the interaction.",
    "Specify all participants and their roles (e.g., 'Dario Webber (RM)').",
    "Quantify key figures, such as the exact concentration risk percentage.",
    "Document the client's specific reason for their decision."
  ]
}