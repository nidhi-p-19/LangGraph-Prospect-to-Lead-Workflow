from __future__ import annotations
from typing import Dict, Any, List
import os
from agents.base import BaseAgent

# ------------------------------------------------------------------
# 📩 Fallback template (used if Gemini is unavailable or errors out)
# ------------------------------------------------------------------
FALLBACK_TEMPLATE = (
    "Subject: {subject}\n\n"
    "Hi {first_name},\n\n"
    "Noticed {company} is {signal_phrase}. We help SaaS teams accelerate outbound with "
    "an AI-led workflow (LangGraph agents) that finds + scores + contacts prospects automatically.\n\n"
    "Would you be open to a 15-min chat on how teams like yours lift pipeline by 20–30% in 30 days?\n\n"
    "— Kalp\n"
    "Analytos.ai"
)

def _fallback_email(lead: Dict[str, Any]) -> Dict[str, str]:
    first_name = (lead.get("contact", "") or "there").split()[0]
    subj = f"{lead.get('company','Your team')} × Analytos.ai — quick idea"
    signal = lead.get("signal", "momentum signals")
    signal_phrase = (
        "hiring for Sales"
        if signal == "hiring_for_sales"
        else "recently funded"
        if signal == "recent_funding"
        else "seeing momentum"
    )
    body = FALLBACK_TEMPLATE.format(
        subject=subj,
        first_name=first_name,
        company=lead.get("company", "your team"),
        signal_phrase=signal_phrase,
    )
    return {"subject": subj, "body": body}


# ------------------------------------------------------------------
# 🤖 OutreachContentAgent
# ------------------------------------------------------------------
class OutreachContentAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ranked = payload.get("ranked_leads", [])
        persona = payload.get("persona", "SDR")
        tone = payload.get("tone", "friendly")
        messages: List[Dict[str, Any]] = []

        # ------------------------------
        # Try Gemini first; fallback if missing
        # ------------------------------
        gemini_key = os.getenv("GEMINI_API_KEY")
        use_gemini = bool(gemini_key)

        if use_gemini:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel("gemini-2.0-flash")
            except Exception as e:
                self._log(
                    "warning",
                    {
                        "msg": "Gemini import/config failed, using fallback",
                        "error": str(e),
                    },
                )
                use_gemini = False

        # ------------------------------
        # Generate emails
        # ------------------------------
        for item in ranked[:10]:
            lead = item["lead"]

            if use_gemini:
                try:
                    prompt = f"""
You are an expert SDR writing short, high-relevance cold emails.

Write one B2B outreach email (<120 words), friendly, concise, outcome-focused.

Company: {lead.get('company')}
Contact: {lead.get('contact')}
Role: {lead.get('role')}
Signal: {lead.get('signal')}
Tone: {tone}
Persona: {persona}

Constraints:
- 1 clear subject line
- 3–5 short sentences
- 1 specific CTA (15-min chat)
- No emojis or buzzwords
Return the result as:
Subject: ...
Body: ...
"""
                    resp = model.generate_content(prompt)
                    text = (getattr(resp, "text", None) or "").strip()

                    if not text:
                        rb = _fallback_email(lead)
                        subject, body = rb["subject"], rb["body"]
                    else:
                        if text.lower().startswith("subject:"):
                            first_line, *rest = text.splitlines()
                            subject = (
                                first_line.split(":", 1)[1].strip()
                                if ":" in first_line
                                else "Quick idea for you"
                            )
                            body = "\n".join(rest).strip()
                        else:
                            subject = "Quick idea for you"
                            body = text
                except Exception as e:
                    self._log(
                        "warning",
                        {
                            "msg": "Gemini call failed, using fallback",
                            "error": str(e),
                        },
                    )
                    rb = _fallback_email(lead)
                    subject, body = rb["subject"], rb["body"]
            else:
                rb = _fallback_email(lead)
                subject, body = rb["subject"], rb["body"]

            # save message
            messages.append(
                {
                    "lead": lead.get("contact"),
                    "to": lead.get("domain", "unknown@unknown.com"),
                    "subject": subject,
                    "email_body": body,
                }
            )

        # Log both summary and full messages for dashboard
        self._log("output", {
            "count": len(messages),
            "gemini_used": use_gemini,
            "messages": messages
        })
        return {"messages": messages}

