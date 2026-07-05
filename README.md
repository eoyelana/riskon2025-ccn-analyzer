# RiskON 2025: AI-Powered Client Contact Note Analyzer

A proof-of-concept solution for the **Julius Baer RiskON 2025 Challenge**. This project uses AI-powered language models to provide real-time quality assurance for manually created Client Contact Notes (CCNs). While the solution is flexible and can work with various LLM providers, we have implemented it using **Perplexity's Sonar API** due to its availability and ease of access for personal use and testing.

<p align="center">
  <img src="./assets/licensed-image.jpeg" alt="AI Contact Note Analyzer Banner" width="600" heignt="300">
</p>


## 1. Challenge Overview

The core challenge is to improve the **completeness and quality** of manually entered Client Contact Notes. High-quality CCNs are critical for regulatory compliance, documenting client interactions, and proving reverse solicitation.

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
* **Reverse Solicitation Detection:** Identifies potential solicitation risks and provides compliance guidance.
* **CCN Type Classification:** Automatically categorizes notes (Portfolio Review, Account Opening, Complaint, etc.).
* **API-First Design:** Built with FastAPI for easy integration into any front-end or CRM system.
* **Developer Friendly:** Adheres to modern coding standards, including `black` formatting and `ruff` linting.

## 3. Tech Stack

This project is built on modern, production-ready components that meet all technical requirements of the challenge.

| Component      | Technology                               | Purpose                                      |
| -------------- | ---------------------------------------- | -------------------------------------------- |
| **Language** | Python 3.9+                              | Core application logic.                      |
| **AI / LLM** | Perplexity Sonar Pro                     | Natural Language Processing & Analysis.      |
| **API Client** | OpenAI SDK                               | For Perplexity API compatibility.            |
| **API Framework**| FastAPI                                  | To expose the analysis logic as a REST API.  |
| **Server** | Uvicorn                                  | High-performance ASGI server.                |
| **Container** | Docker                                   | For packaging the app for K8s deployment.    |
| **Code Quality** | Black, Ruff                              | Linting and code formatting.                 |
| **Testing** | Pytest                                   | For writing unit and integration tests.      |
| **Environment** | python-dotenv                            | Secure API key management.                   |

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

4.  **Configure your API key:**
    
    The repository includes a `.env.template` file for easy setup. Simply:
    
    a. Copy the template file:
    ```
    cp .env.template .env
    ```
    
    b. Open the `.env` file and add your Perplexity API key:
    ```
    PERPLEXITY_API_KEY="your_api_key_here"
    ```
    
    **Note:** The `.env` file is included in `.gitignore` to protect your sensitive credentials.


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
  "sme_judgement": "Poor example",
  "sme_comments": [
    "The CCN lacks sufficient detail for audit and compliance purposes. Key information is missing or ambiguous: participant roles are not fully specified, the business context and decision rationale are minimal, and the location, channel, and timing of the interaction are not documented. The note does not explain how the client was informed of the risks or how the decision to accept concentration risk was reached. There is no documentation of whether the discussion was at the client's initiative or if any advice was given, which is critical for reverse solicitation and cross-border compliance."
  ],
  "completeness": {
    "who": "Partially complete",
    "what": "Partially complete",
    "why": "Missing",
    "where": "Missing",
    "when": "Missing"
  },
  "ccn_type": "Portfolio Review",
  "possible_solicitation": {
    "value": true,
    "reason": "The note does not clarify whether the discussion of concentration risk in Nvidia was initiated by the client or if the RM provided advice or recommendations. This ambiguity creates solicitation risk, especially if the RM initiated the call or discussion.",
    "rm_next_action": "Add a statement clarifying the origin of the discussion, e.g., 'At the client's exclusive request, we discussed the concentration risk in Nvidia.' If the RM provided advice, document the client's request for such advice and the rationale for accepting the risk."
  },
  "missing_info": [
    "List all participants and their roles (e.g., 'Sabrina (POA)', 'Mr Martin (AH)', 'RM').",
    "Specify the business context: what specific portfolio issues, risks, or decisions were discussed beyond 'concentration risk in Nvidia'.",
    "Document the client's rationale for accepting the risk and how the decision was reached.",
    "Record the location (country, city), communication channel (e.g., phone, email), and whether cross-border rules apply.",
    "Include the date and time of the interaction.",
    "Clarify whether the discussion was at the client's initiative (reverse solicitation) or if the RM initiated the topic."
  ],
  "follow_up_questions": [
    "Who participated in the call? Please specify all names and roles.",
    "What specific topics, risks, or decisions were discussed regarding the portfolio?",
    "What was the client's rationale for accepting the concentration risk in Nvidia? How was this risk explained and discussed?",
    "Where did the interaction take place (country, city), and what channel was used (phone, email, etc.)?",
    "When did the interaction occur (date and time)?",
    "Did the client request this discussion, or did the RM initiate it? Please clarify to address reverse solicitation risk."
  ]
}