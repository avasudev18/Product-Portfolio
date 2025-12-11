import streamlit as st

st.set_page_config(page_title="Customer Success & Growth", page_icon="📊", layout="wide")

st.title("Executive Leadership in Customer Success & Growth")

st.markdown(
    """
Directed global **Customer Success and Growth** operations using data-driven renewal forecasting,
expansion playbooks, voice-of-customer (VoC) analytics, automated onboarding workflows, and
KPI-driven dashboards (NRR, GRR, CAC, LTV, CSAT, SLA)—accelerating revenue growth and reducing churn
across mid-market and enterprise portfolios.
"""
)

st.divider()

st.subheader("Mid-Market Portfolio Transformation")

st.markdown(
    """
As **Director of Customer Success**, I inherited a mid-market portfolio operating in a high-growth
environment with:

- Rising customer volume  
- Increasing operational complexity  
- Inconsistent engagement cadence  
- Limited automation and fragmented tooling  

Resolution cycles averaged **35 days**, and there was no unified performance framework to govern
service quality, retention risk, or expansion readiness.
"""
)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
I designed and implemented a **structured engagement model** across 20+ active tenants, including:

- Predictable weekly, bi-weekly, monthly, and quarterly cadences  
- A weighted performance framework governing CSAT, resolution speed, escalation control, and proactive actions  
- A **30-60-90 execution model** to ensure continuous value realization  

In parallel, I led **automated HDA ingestion**, expanded analytics deployments, and drove GenAI
readiness classification across 25 customers—ensuring the portfolio scaled with data-driven precision.
        """
    )

with col2:
    st.markdown(
        """
**Repeatable, Scalable, Reusable (RSR) Impact & KPIs**

- ✅ **0** SLA breaches  
- ✅ Average resolution time reduced **35 days → under 5 days**  
- ✅ First Response Time (FRT): **< 5 minutes**  
- ✅ First Contact Resolution (FCR): significantly improved  
- ✅ **80%** reduction in escalation rate  

Customer Success now operates as a **scalable revenue engine and churn-prevention system**, positioning
the business for future-ready, AI-enabled growth.
        """
    )

st.link_button(
    "📄 View Leadership Framework Deck",
    "https://avasudev18.github.io/PFolioAV.github.io/Mid-Market-CSM-Weekly-Review-Apri-20.pdf",
)
