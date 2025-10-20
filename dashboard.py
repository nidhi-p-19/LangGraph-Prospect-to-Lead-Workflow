import json
from pathlib import Path
import streamlit as st

# -------------------------------------------------------
# 🎨 Page Setup
# -------------------------------------------------------
st.set_page_config(
    page_title="LangGraph Prospect-to-Lead Dashboard",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 LangGraph Prospect-to-Lead Dashboard")
st.markdown("### End-to-End Campaign Metrics")

# -------------------------------------------------------
# 📊 Load Feedback Trainer Metrics
# -------------------------------------------------------
data_path = Path(".runs") / "feedback_trainer.log"
if not data_path.exists():
    st.error("⚠️ No feedback_trainer.log found. Run your workflow first!")
    st.stop()

metrics, recommendations = {}, []
with open(data_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            entry = json.loads(line.strip())
            if not isinstance(entry, dict):
                continue
            if entry.get("kind") == "metrics":
                metrics = entry.get("payload", {})
            elif entry.get("kind") == "recommendations":
                recommendations = entry.get("payload", [])
        except json.JSONDecodeError:
            continue

# -------------------------------------------------------
# 📈 Metrics Summary
# -------------------------------------------------------
open_rate = metrics.get("open_rate", 0) * 100
click_rate = metrics.get("click_rate", 0) * 100
reply_rate = metrics.get("reply_rate", 0) * 100
meeting_rate = metrics.get("meeting_rate", 0) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("📬 Open Rate", f"{open_rate:.1f}%")
col2.metric("🔗 Click Rate", f"{click_rate:.1f}%")
col3.metric("💬 Reply Rate", f"{reply_rate:.1f}%")
col4.metric("📅 Meeting Rate", f"{meeting_rate:.1f}%")

# -------------------------------------------------------
# 📊 Progress Bars
# -------------------------------------------------------
st.divider()
st.subheader("📈 Performance Overview")

progress_cols = st.columns(4)
progress_cols[0].progress(open_rate / 100, text="Open Rate")
progress_cols[1].progress(click_rate / 100, text="Click Rate")
progress_cols[2].progress(reply_rate / 100, text="Reply Rate")
progress_cols[3].progress(meeting_rate / 100, text="Meeting Rate")

# -------------------------------------------------------
# 🧠 Recommendations
# -------------------------------------------------------
st.divider()
st.subheader("🧠 FeedbackTrainer Recommendations")

if recommendations:
    for i, r in enumerate(recommendations, start=1):
        st.markdown(f"**{i}.** {r}")
else:
    st.info("No recommendations yet. Try running another workflow cycle.")

# -------------------------------------------------------
# ✉️ Outreach Emails Section
# -------------------------------------------------------
st.divider()
st.subheader("✉️ Generated Outreach Emails")

emails_path = Path(".runs") / "outreach_content.log"
if emails_path.exists():
    with open(emails_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        emails = []
        for l in lines:
            try:
                emails.append(json.loads(l))
            except Exception:
                continue

        shown = 0
        for entry in emails:
            if isinstance(entry, dict) and "output" in entry:
                msgs = entry["output"].get("messages", [])
                for msg in msgs[:5]:
                    shown += 1
                    subject = msg.get("subject", "Untitled")
                    body = msg.get("email_body", "")
                    to = msg.get("to", "unknown@unknown.com")
                    lead = msg.get("lead", "N/A")

                    with st.expander(f"💌 {shown}. {subject}", expanded=False):
                        st.markdown(f"**To:** {to}")
                        st.markdown(f"**Lead:** {lead}")
                        st.markdown("---")
                        st.write(body)

            if shown >= 5:
                break

    if shown == 0:
        st.info("No generated emails found yet. Run OutreachContentAgent first.")
else:
    st.info("No outreach_content.log found yet. Run your workflow first.")

# -------------------------------------------------------
# 🦾 Footer
# -------------------------------------------------------
st.divider()
st.caption("Built with ❤️ using LangGraph + Gemini 2.0 + Streamlit")
