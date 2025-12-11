import streamlit as st
from pathlib import Path

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Anil Vasudevakurup | Product Management Portfolio",
    page_icon="💼",
    layout="wide"
)

# ---------------------------------------------------------
# PATHS AND PROFILE DATA
# ---------------------------------------------------------
BASE_DIR = Path(__file__).parent               # PFolio/
HEADSHOT_PATH = BASE_DIR / "assets" / "anil_headshot.jpg"

NAME = "Anil Vasudevakurup"
ROLE = (
    "Director of Product Management | SaaS, AI, Field Service, "
    "ERP Integrations | Customer Success Leader"
)
LOCATION = "Denver, CO"
EMAIL = "your.email@example.com"   # TODO: update
LINKEDIN_URL = "https://www.linkedin.com/in/anil-vasudevakurup/"


def main():
    # -----------------------------------------------------
    # HEADER SECTION
    # -----------------------------------------------------
    col_img, col_text = st.columns([1, 3])

    with col_img:
        if HEADSHOT_PATH.is_file():
            st.image(str(HEADSHOT_PATH), use_container_width=True)
        else:
            # Fallback avatar if image is not found
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
    # (Optional) CORE EXPERTISE SECTION
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
    # BUTTONS AT THE BOTTOM
    # -----------------------------------------------------
    st.divider()
    st.subheader("Explore the Portfolio")

    accessible_button_style = """
        display: inline-block;
        padding: 12px 22px;
        margin: 6px 6px 12px 0px;
        background-color: #1f77b4;      /* Accessible blue */
        color: #ffffff !important;
        text-decoration: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 500;
    """

    st.markdown(
        f"""
        <a href="?page=Bio" style="{accessible_button_style}">🧑‍💼 Bio</a>
        <a href="?page=Live_Implementations" style="{accessible_button_style}">💼 Live Implementations</a>
        <a href="?page=Customer_Success_Leadership" style="{accessible_button_style}">📊 Customer Success Leadership</a>
        <br>
        <a href="?page=Thought_Leadership_&_Innovation_Lab" style="{accessible_button_style}">🤖 Innovation Lab</a>
        <a href="?page=Experience_&_Education" style="{accessible_button_style}">📜 Experience & Education</a>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # FOOTER INFO
    # -----------------------------------------------------
    st.divider()
    st.info(
        "Use the sidebar or the navigation buttons above to explore the portfolio: "
        "Bio, live implementations, customer success leadership, innovation lab, "
        "and full experience & education."
    )


if __name__ == "__main__":
    main()
