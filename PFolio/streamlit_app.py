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

    st.divider()

    # -----------------------------------------------------
    # CORE EXPERTISE
    # -----------------------------------------------------
    st.subheader("Core Expertise")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
### Product Leadership
- Product strategy & long-range vision  
- Outcome-driven roadmapping & prioritization  
- Cross-functional collaboration (Eng, Design, CS, Sales)  
- Go-to-market planning & launch execution  

### AI / Data
- AI agents & generative AI workflows  
- Retrieval-Augmented Generation (RAG) pipelines  
- Recommendation engines & personalization  
- Predictive analytics & forecasting  
"""
        )

    with c2:
        st.markdown(
            """
### Enterprise Systems
- Oracle Field Service (OFS/OFSC)  
- ERP & commerce integrations (Infor, Karmak, SAP, DST)  
- Large-scale SaaS platform design  

### Customer Success & Revenue
- Onboarding & adoption frameworks  
- Renewal, expansion & churn prevention strategy  
- KPI-driven operations (NRR, GRR, CSAT, SLA)  
"""
        )

    st.divider()

    # -----------------------------------------------------
    # NAVIGATION CARDS TO OTHER PAGES
    # -----------------------------------------------------
    st.subheader("Explore the Portfolio")

    # First row: Bio, Live Implementations, Customer Success
    row1 = st.columns(3)

    with row1[0]:
        st.markdown(
            """
            <div style="
                padding:16px;
                border-radius:12px;
                border:1px solid #e0e0e0;
                background-color:#fafafa;
                height:100%;
            ">
                <h4>🧑‍💼 Bio</h4>
                <p style="font-size:0.9rem;">
                    Learn about Anil's background, leadership philosophy,
                    and approach to product strategy.
                </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<a href="?page=Bio"><button style="padding:6px 12px;">Open</button></a>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with row1[1]:
        st.markdown(
            """
            <div style="
                padding:16px;
                border-radius:12px;
                border:1px solid #e0e0e0;
                background-color:#fafafa;
                height:100%;
            ">
                <h4>💼 Live Implementations</h4>
                <p style="font-size:0.9rem;">
                    Case studies in AI commerce, parts catalog integration,
                    field service transformation, and dynamic pricing.
                </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<a href="?page=Live_Implementations">'
            '<button style="padding:6px 12px;">Open</button></a>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with row1[2]:
        st.markdown(
            """
            <div style="
                padding:16px;
                border-radius:12px;
                border:1px solid #e0e0e0;
                background-color:#fafafa;
                height:100%;
            ">
                <h4>📊 Customer Success Leadership</h4>
                <p style="font-size:0.9rem;">
                    Portfolio transformation, operational frameworks,
                    and KPI-driven customer success at scale.
                </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<a href="?page=Customer_Success_Leadership">'
            '<button style="padding:6px 12px;">Open</button></a>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Second row: Innovation Lab, Experience & Education
    row2 = st.columns(2)

    with row2[0]:
        st.markdown(
            """
            <div style="
                padding:16px;
                border-radius:12px;
                border:1px solid #e0e0e0;
                background-color:#fafafa;
                height:100%;
            ">
                <h4>🤖 Thought Leadership & Innovation Lab</h4>
                <p style="font-size:0.9rem;">
                    Multi-agent AI workflows, prototypes, and
                    future-facing product experiments.
                </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<a href="?page=Thought_Leadership_&_Innovation_Lab">'
            '<button style="padding:6px 12px;">Open</button></a>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with row2[1]:
        st.markdown(
            """
            <div style="
                padding:16px;
                border-radius:12px;
                border:1px solid #e0e0e0;
                background-color:#fafafa;
                height:100%;
            ">
                <h4>📜 Experience & Education</h4>
                <p style="font-size:0.9rem;">
                    Career milestones, certifications, and formal
                    academic background.
                </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<a href="?page=Experience_&_Education">'
            '<button style="padding:6px 12px;">Open</button></a>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # -----------------------------------------------------
    # FOOTER INFO
    # -----------------------------------------------------
    st.info(
        "Use the sidebar or the cards above to navigate Anil's portfolio: "
        "Bio, live product implementations, customer success leadership, "
        "innovation lab, and full experience and education."
    )


if __name__ == "__main__":
    main()
