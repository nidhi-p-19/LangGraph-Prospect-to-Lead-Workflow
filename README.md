# LangGraph Prospect-to-Lead 

### An AI-powered autonomous system to discover, enrich, score, and contact B2B prospects — then learn from campaign feedback.

---

## 🧩 Overview

This project implements a **LangGraph-based multi-agent system** for B2B outbound automation.  
It dynamically builds and executes a workflow of AI agents that perform:

1. **Prospect Search** – Find ideal prospects via Apollo & Clay APIs  
2. **Data Enrichment** – Add company & contact context using Clearbit or People Data Labs  
3. **Scoring** – Rank prospects using ICP (Ideal Customer Profile) rules  
4. **Outreach Content** – Generate personalized emails using Google Gemini (or OpenAI)  
5. **Outreach Execution** – Send emails automatically (SendGrid or Apollo API)  
6. **Response Tracking** – Monitor open, click, reply, and meeting events  
7. **Feedback Training** – Analyze performance metrics & suggest optimization actions  

The system continuously refines itself based on real campaign outcomes — simulating an AI-SDR that never stops improving.

---

## 🧠 Architecture

```
ProspectSearch → DataEnrichment → Scoring → OutreachContent → OutreachExecutor → ResponseTracker → FeedbackTrainer
```

Each node = one **LangGraph agent** defined in the `workflows/workflow.json` file.

| Agent | Description |
|--------|-------------|
| `ProspectSearchAgent` | Finds prospects via Clay & Apollo APIs |
| `DataEnrichmentAgent` | Enriches lead data (Clearbit/LinkedIn) |
| `ScoringAgent` | Scores leads based on ICP parameters |
| `OutreachContentAgent` | Generates personalized cold emails (Gemini / GPT-4) |
| `OutreachExecutorAgent` | Sends messages via SendGrid or Apollo |
| `ResponseTrackerAgent` | Tracks campaign metrics |
| `FeedbackTrainerAgent` | Evaluates metrics & refines strategy |

---

## ⚙️ Installation

### 1️⃣ Clone this repository
```bash
git clone https://github.com/nidhi-p-19/LangGraph-Prospect-to-Lead-Workflow
cd LangGraph-Prospect-to-Lead-Workflow
```

### 2️⃣ Create & activate virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate   # On Windows
source .venv/bin/activate  # On Mac/Linux
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create your `.env` file
```bash
GEMINI_API_KEY="your_google_gemini_api_key"
APOLLO_API_KEY="your_apollo_api_key"
CLAY_API_KEY="your_clay_api_key"
CLEARBIT_KEY="your_clearbit_api_key"
SENDGRID_API_KEY="your_sendgrid_api_key"

GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON=service_account.json
SHEET_ID="your_google_sheet_id"

CHROMA_DIR=.chroma
```
(You can leave unused keys blank if you only want to test locally.)

---

## 🧩 How to Run

### ▶️ 1. Execute the workflow
```bash
python langgraph_builder.py --workflow workflows/workflow.json --run
```
This reads the JSON workflow, constructs the graph, executes all nodes sequentially, and prints the final output (recommendations, metrics, and results).

### 📊 2. Launch the Streamlit Dashboard
```bash
streamlit run dashboard.py
```
View campaign performance, open rates, and recommendations interactively.

---

## 🧰 Project Structure
```bash
prospect-langgraph/
├── agents/                 # Modular agent scripts
│   ├── prospect_search.py
│   ├── enrichment.py
│   ├── scoring.py
│   ├── outreach_content.py
│   ├── outreach_executor.py
│   ├── response_tracker.py
│   └── feedback_trainer.py
├── tools/                  # API clients & helper utilities
├── utils/                  # Logging, config, and data utilities
├── workflows/              # JSON workflow definitions
│   └── workflow.json
├── dashboard.py            # Streamlit analytics dashboard
├── langgraph_builder.py    # Workflow builder & executor
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧩 Example Workflow Snippet
```json
{
  "workflow_name": "OutboundLeadGeneration",
  "description": "End-to-end AI agent workflow to find, contact, and qualify leads",
  "steps": [
    {
      "id": "prospect_search",
      "agent": "ProspectSearchAgent",
      "inputs": {
        "icp": { "industry": "SaaS", "location": "USA" },
        "signals": ["recent_funding", "hiring_for_sales"]
      },
      "tools": [
        { "name": "ClayAPI", "config": { "api_key": "{{CLAY_API_KEY}}" } },
        { "name": "ApolloAPI", "config": { "api_key": "{{APOLLO_API_KEY}}" } }
      ]
    }
  ]
}
```

---

## 📈 Sample Output
```json
{
  "recommendations": [
    "Tighten ICP to focus 100–500 employees; add funding signal filter."
  ],
  "metrics": {
    "open_rate": 0.66,
    "click_rate": 0.16,
    "reply_rate": 0.33,
    "meeting_rate": 0.16
  }
}
```

---

## 💡 Future Extensions
- Add multi-threaded async pipeline execution  
- Integrate CRMs (HubSpot, Pipedrive) for real lead syncing  
- Deploy as API (FastAPI + LangGraph SDK)  
- Integrate fine-tuned LLMs for domain-specific outreach  
---

🚀 Built with **Python**, **LangGraph**, and **Gemini** — for autonomous, data-driven prospecting.
'''

with open('README.md', 'w') as f:
    f.write(content)

'README.md'
