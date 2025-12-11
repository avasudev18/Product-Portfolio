import streamlit as st

st.set_page_config(
    page_title="Thought Leadership & Innovation Lab",
    page_icon="🤖",
    layout="wide"
)

st.title("Thought Leadership & Innovation Lab")

st.markdown(
    """
This section highlights **AI-driven product thinking**, multi-agent workflows, and innovation
initiatives that reimagine how products are conceived, built, and scaled.
"""
)

st.divider()

# ---------- Agentic Workflow for Interview Preparation ----------
st.subheader("AI-Powered Agentic Workflow to Optimize Interview Preparation")

st.markdown(
    """
This multi-agent workflow automatically inspects a candidate's job applications, detects interview
invitations, and prepares personalized interview readiness materials for each role (e.g., Product Manager,
Director/Principal PM, Customer Success Leader, Field Service/ERP Integration roles, Digital Commerce PM).

The workflow includes:
1️⃣ **Job Intake & Interview Detection Agent**  
2️⃣ **Role & JD Analysis Agent**  
3️⃣ **Company Research Agent**  
4️⃣ **Recruiter & Hiring Manager Analysis Agent**  
5️⃣ **Core Interview Question Generator Agent**  
6️⃣ **Quantified STAR Story Builder Agent**  
7️⃣ **Product Deep Dive & 30-60-90 Day Plan Agent**  
8️⃣ **Mock Interview Simulation Agent**  
"""
)

st.image(
    "https://avasudev18.github.io/PFolioAV.github.io/feature/PM%20Interview%20Prep%20Agentic%20Workflow.png",
    caption="Multi-agent interview preparation workflow",
    use_container_width=True,
)

st.markdown(
    """
**What’s next?**

1. Run the automation  
2. Monitor, test, evaluate, and improve  
3. Integrate with your broader product and talent tooling ecosystem  
"""
)

st.divider()

# ---------- SmartGardener ----------
st.subheader("Reimagining the Future: SmartGardener – Personalized Gardening Assistant")

st.markdown(
    """
**SmartGardener** is a personalized gardening assistant app designed to empower home gardeners with
intelligent insights and practical tools to manage both indoor and outdoor plants.

By leveraging **real-time location data**, seasonal patterns, and plant health diagnostics, the app
provides tailored recommendations to optimize plant care and ensure healthy growth.

Throughout the product lifecycle, I incorporated **generative AI** at each stage to accelerate ideation,
improve feature design, and elevate user experience.
"""
)

c1, c2 = st.columns(2)

with c1:
    st.image(
        "https://avasudev18.github.io/PFolioAV.github.io/Prototypes/Mobile/SmartGardner.jpeg",
        caption="SmartGardener – mobile prototype UI",
        use_container_width=True,
    )

with c2:
    st.image(
        "https://avasudev18.github.io/PFolioAV.github.io/Prototypes/Mobile/GardenApp_Wire.png",
        caption="SmartGardener – early wireframes",
        use_container_width=True,
    )

st.markdown(
    """
**Design & Product Artefacts**

- 📄 [1. Functional Design Document](https://avasudev18.github.io/PFolioAV.github.io/Prototypes/Mobile/FunctionalDesginDocument.html)  
- 🧩 [2. Simple Wireframe](https://avasudev18.github.io/PFolioAV.github.io/Prototypes/Mobile/GardenApp_Wire.png)  
- 📱 [3. Interactive Prototype](https://avasudev18.github.io/PFolioAV.github.io/Prototypes/Mobile/GardenApp.html)  
- 📝 [4. GardenApp (Beta) Deck](https://avasudev18.github.io/PFolioAV.github.io/Prototypes/Mobile/Mobile%20App.pdf)  
- 🧠 [5. SWOT Analysis](https://avasudev18.github.io/PFolioAV.github.io/Prototypes/Mobile/SWOT.pdf)  
- 🗺️ [6. Strategy Roadmap](https://avasudev18.github.io/PFolioAV.github.io/Prototypes/Mobile/Strategy%20Roadmap.pdf)  
"""
)
