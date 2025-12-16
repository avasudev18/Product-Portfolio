import streamlit as st
from pathlib import Path

#-----------------------NEW---------------------------------

def custom_sidebar():
    st.sidebar.title("Portfolio Navigation")

    # Normal pages (still shown automatically by Streamlit)
    st.sidebar.divider()

    # ---- Custom submenu simulation ----
    with st.sidebar.expander("🤖 Thought Leadership & Innovation Lab", expanded=False):
        st.page_link(
            "pages/3_🤖_Thought_Leadership_&_Innovation_Lab.py",
            label="AI-Powered Agentic Interview Workflow",
            icon="🧠"
        )
        st.page_link(
            "pages/5_PM_Interview_Prep_Agentic_Workflow.py",
            label="SmartGardener – Personalized Gardening Assistant",
            icon="🌱"
        )

    st.sidebar.divider()

#------------------------------End NEW-----------------------------------

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Anil Vasudevakurup | Product Management Portfolio",
    page_icon="💼",
    layout="wide"
)
custom_sidebar()


# ---------------------------------------------------------
# PATHS AND PROFILE DATA
# ---------------------------------------------------------
BASE_DIR = Path(__file__).parent
HEADSHOT_PATH = BASE_DIR / "assets" / "anil_headshot.jpg"

NAME = "Anil Vasudevakurup"
ROLE = (
    "Director of Product Management | SaaS, AI, Field Service, "
    "ERP Integrations | Customer Success Leader"
)
LOCATION = "Denver, CO"
EMAIL = "anilvasudev2001@gmail.com"
LINKEDIN_URL = "https://www.linkedin.com/in/anil-vasudevakurup/"

# Optional: helper links (may work depending on hosting)
# If they don’t work on your hosting, users can still navigate via sidebar.
PAGE_LINKS = {
    "💼 Live Implementations": "Live_Implementations",
    "📊 Customer Success Leadership": "Customer_Success_Leadership",
    "🤖 Thought Leadership & Innovation Lab": "Thought_Leadership_&_Innovation_Lab",
    "📜 Experience & Education": "Experience_&_Education",
}


def main():
    # -----------------------------------------------------
    # HEADER SECTION
    # -----------------------------------------------------
    col_img, col_text = st.columns([1, 3])

    with col_img:
        if HEADSHOT_PATH.is_file():
            st.image(str(HEADSHOT_PATH), use_container_width=True)
        else:
            st.markdown(
                """
                <div style="text-align:center; font-size:60px;">👤</div>
                <p style="text-align:center; color:gray;">
                    Upload <code>assets/anil_headshot.jpg</code> to show headshot.
                </p>
                """,
                unsafe_allow_html=True,
            )

    with col_text:
        st.title(NAME)
        st.write(ROLE)
        st.markdown(
            f"**{LOCATION}** • 📧 `{EMAIL}` • "
            f"[LinkedIn]({LINKEDIN_URL})"
        )

    st.divider()

    # -----------------------------------------------------
    # QUICK LINKS
    # -----------------------------------------------------
    st.subheader("Quick Links")

    q1, q2, q3 = st.columns(3)
    with q1:
        st.link_button("🔗 LinkedIn", LINKEDIN_URL)
    with q2:
        st.link_button("📄 Download Resume", "#", help="Replace with resume URL")
    with q3:
        st.link_button(
            "🌐 Original Portfolio Site",
            "https://avasudev18.github.io/PFolioAV.github.io/index.html",
        )

    # -----------------------------------------------------
    # CORE EXPERTISE SECTION
    # -----------------------------------------------------
    st.divider()
    st.subheader("Core Expertise")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
### Product Leadership
- Product strategy & long-range vision  
- Outcome-driven roadmapping & prioritization  
- Cross-functional collaboration (Eng, Design, CS, Sales)  

### AI / Data
- AI agents & generative AI workflows  
- Retrieval-Augmented Generation (RAG)  
- Recommendation engines & forecasting  
"""
        )
    with c2:
        st.markdown(
            """
### Enterprise Systems
- Oracle Field Service (OFS/OFSC)  
- ERP & commerce integrations (Infor, Karmak, SAP, DST)  

### Customer Success & Revenue
- Onboarding & adoption frameworks  
- Renewal, expansion & churn prevention  
- KPI-driven operations (NRR, GRR, CSAT, SLA)  
"""
        )

    # -----------------------------------------------------
    # NAVIGATION (Sidebar-driven)
    # -----------------------------------------------------
    st.divider()
    st.subheader("Explore the Portfolio")

    st.info(
        "Use the **sidebar** to navigate. Under **🤖 Thought Leadership & Innovation Lab**, "
        "you’ll see the subpages:\n"
        "- AI Powered Agentic Interview Workflow\n"
        "- SmartGardener – Personalized Gardening Assistant"
    )

    # Optional shortcut buttons (works on many Streamlit deployments)
    # If your hosting doesn't support query navigation, these still serve as clear calls-to-action.
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.link_button("💼 Live Implementations", "/Live_Implementations")
    with b2:
        st.link_button("📊 Customer Success", "/Customer_Success_Leadership")
    with b3:
        st.link_button("🤖 Innovation Lab", "/Thought_Leadership_&_Innovation_Lab")
    with b4:
        st.link_button("📜 Experience", "/Experience_&_Education")

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------
    st.divider()
    st.caption("© Anil Vasudevakurup • Streamlit portfolio")


if __name__ == "__main__":
    main()
