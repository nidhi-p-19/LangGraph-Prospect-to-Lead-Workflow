from __future__ import annotations
import os, random
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

def is_mock() -> bool:
    keys = ["APOLLO_API_KEY", "CLAY_API_KEY", "CLEARBIT_KEY", "SENDGRID_API_KEY", "OPENAI_API_KEY"]
    return not any(os.getenv(k) for k in keys)

MOCK_NAMES = [
    ("AcmeSoft", "Dana Fox"), ("BlueSkyCRM", "Jordan Singh"),
    ("NimbusBI", "Avery Patel"), ("MetricHub", "Taylor Kim"),
    ("Quantico SaaS", "Riley Gupta"), ("SignalOps", "Casey Rao")
]

def mock_leads(n=5) -> List[Dict[str, Any]]:
    out = []
    for i in range(n):
        company, person = random.choice(MOCK_NAMES)
        out.append({
            "company": company,
            "contact_name": person,
            "email": f"{person.split()[0].lower()}@{company.replace(' ', '').lower()}.com",
            "linkedin": f"https://www.linkedin.com/in/{person.split()[0].lower()}-{i}",
            "signal": random.choice(["recent_funding", "hiring_for_sales", "new_cto", "product_launch"]),
        })
    return out

def mock_enrich(leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    roles = ["VP Sales", "Head of RevOps", "CTO", "Director of Demand Gen", "COO"]
    stacks = [["HubSpot","Salesforce"], ["Snowflake","dbt"], ["Segment","Marketo"], ["Amplitude","Mixpanel"]]
    out = []
    for L in leads:
        out.append({
            "company": L["company"],
            "contact": L["contact_name"],
            "role": random.choice(roles),
            "technologies": random.choice(stacks),
            "domain": f"{L['company'].replace(' ', '').lower()}.com"
        })
    return out

def mock_send(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    res = []
    for i, m in enumerate(messages):
        res.append({"lead": m.get("lead"), "status": "sent", "message_id": f"mock-{i}"})
    return res

def mock_responses(sent_status: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    import random
    for s in sent_status:
        out.append({
            "lead": s["lead"],
            "opened": random.random() < 0.7,
            "clicked": random.random() < 0.3,
            "replied": random.random() < 0.15,
            "booked_meeting": random.random() < 0.05,
        })
    return out

def mock_recos(metrics: Dict[str, float]) -> List[str]:
    recs = []
    if metrics.get("open_rate", 0) < 0.3:
        recs.append("Test punchier subject lines with pain + outcome.")
    if metrics.get("reply_rate", 0) < 0.05:
        recs.append("Tighten ICP: focus 100–500 employees, highlight RevOps pain.")
    if metrics.get("click_rate", 0) < 0.1:
        recs.append("Add single CTA link early; reduce word count by 25%.")
    if not recs:
        recs.append("Scale volume 2x; current variant performing adequately.")
    return recs

class ApolloClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("APOLLO_API_KEY")
    def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        if is_mock():
            return mock_leads(10)
        raise NotImplementedError("Apollo live client not implemented in this scaffold.")

class ClayClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CLAY_API_KEY")
    def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        if is_mock():
            return mock_leads(8)
        raise NotImplementedError("Clay live client not implemented in this scaffold.")

class ClearbitClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CLEARBIT_KEY")
    def enrich(self, email: str) -> Dict[str, Any]:
        if is_mock():
            return {"role": "VP Sales", "technologies": ["Salesforce","Outreach"]}
        raise NotImplementedError("Clearbit live client not implemented in this scaffold.")

class SendGridClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SENDGRID_API_KEY")
    def send_email(self, to_email: str, subject: str, body: str) -> Dict[str, Any]:
        if is_mock():
            return {"status": "sent", "id": f"sg-mock"}
        raise NotImplementedError("SendGrid live client not implemented in this scaffold.")

class GoogleSheetsClient:
    def __init__(self, sheet_id: Optional[str] = None):
        self.sheet_id = sheet_id or os.getenv("SHEET_ID")
    def append_recommendations(self, rows: List[List[str]]) -> None:
        if is_mock():
            print("[MOCK] Writing to sheet:", rows[:2], "...")
            return
        raise NotImplementedError("Google Sheets live client not implemented in this scaffold.")
