# LangGraph Prospect-to-Lead (Analytos.ai)

End-to-end **LangGraph** agent workflow that autonomously discovers, enriches, scores, and contacts B2B prospects (USA, $20M–$200M rev) and learns over time via a **FeedbackTrainer**.

## Tech Stack
- LangGraph + LangChain
- OpenAI (content), Apollo/Clay (search), Clearbit/PDL (enrichment), SendGrid (delivery)
- Google Sheets (feedback)
- Mock mode works without any API keys

## Repo Layout
```
prospect-langgraph/
├── agents/
│   ├── base.py
│   ├── prospect_search.py
│   ├── enrichment.py
│   ├── scoring.py
│   ├── outreach_content.py
│   ├── outreach_executor.py
│   ├── response_tracker.py
│   └── feedback_trainer.py
├── tools/
│   └── clients.py
├── utils/
│   └── logger.py
├── workflows/
│   └── workflow.json
├── langgraph_builder.py
├── requirements.txt
├── .env.example
└── README.md
```

## Quickstart
```bash
cp .env.example .env
pip install -r requirements.txt
python langgraph_builder.py --workflow workflows/workflow.json --run
```

Outputs/logs are written under `.runs/`.
