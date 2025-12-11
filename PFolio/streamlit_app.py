import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Anil Vasudevakurup | Product Management Portfolio",
    page_icon="💼",
    layout="wide"
)

# ----- PATHS -----
BASE_DIR = Path(__file__).parent          # This will be PFolio/
HEADSHOT_PATH = BASE_DIR / "assets" / "anil_headshot.jpg"

# ----- PROFILE DATA -----
NAME = "Anil Vasudevakurup"
ROLE = "Director of Product Management | SaaS, AI, Field Service, ERP Integrations | Customer Success Leader"
LOCATION = "Denver, CO"
EMAIL = "your.email@example.com"
LINKEDIN_URL = "https://www.linkedin.com/in/anil-vasudevakurup/"


def main():
    cols = st.columns([1, 3])

    # ---- IMAGE COLUMN ----
    with cols[0]:
        if HEADSHOT_PATH.is_file():
            st.image(str(HEADSHOT_PATH), use_container_width=True)
        else:
            # fallback icon if something’s still wrong
            st.markdown(
                """
                <div style="font-size:60px; text-align:center;">👤</div>
                <p style="text-align:center; color:gray;">
                    Headshot not found at:<br>
                    <code>PFolio/assets/anil_headshot.jpg</code>
                </p>
                """,
                unsafe_allow_html=True,
            )

    # ---- TEXT COLUMN ----
    with cols[1]:
        st.title(NAME)
        st.write(ROLE)
        st.markdown(
            f"**{LOCATION}** • 📧 `{EMAIL}` • [LinkedIn]({LINKEDIN_URL})"
        )

st.divider()
st.subheader("Explore the Portfolio")

# Create 5 cards in a grid layout
card_cols = st.columns(3)

with card_cols[0]:
    st.markdown(
        """
        <div style="padding:15px; border-radius:10px; border:1px solid #ddd;">
            <h4>🧑‍💼 Bio</h4>
            <p>Professional background, values, and leadership philosophy.</p>
            <a href="/Bio" target="_self">
                <button style="padding:6px 12px;">Open</button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with card_cols[1]:
    st.markdown(
        """
        <div style="padding:15px; border-radius:10px; border:1px solid #ddd;">
            <h4>💼 Live Implementations</h4>
            <p>Case studies on AI commerce, OFS, ERP integrations, and digital transformation.</p>
            <a href="/Live_Implementations" target="_self">
                <button style="padding:6px 12px;">Open</button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with card_cols[2]:
    st.markdown(
        """
        <div style="padding:15px; border-radius:10px; border:1px solid #ddd;">
            <h4>📊 Customer Success Leadership</h4>
            <p>Portfolio transformation, revenue growth, and NRR/GRR frameworks.</p>
            <a href="/Customer_Success_Leadership" target="_self">
                <button style="padding:6px 12px;">Open</button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Second row
card_cols_2 = st.columns(2)

with card_cols_2[0]:
    st.markdown(
        """
        <div style="padding:15px; border-radius:10px; border:1px solid #ddd;">
            <h4>🤖 Innovation Lab</h4>
            <p>AI agents, prototypes, product research, and future-thinking workflows.</p>
            <a href="/Thought_Leadership_&_Innovation_Lab" target="_self">
                <button style="padding:6px 12px;">Open</button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with card_cols_2[1]:
    st.markdown(
        """
        <div style="padding:15px; border-radius:10px; border:1px solid #ddd;">
            <h4>📜 Experience & Education</h4>
            <p>Career milestones, certifications, and academic journey.</p>
            <a href="/Experience_&_Education" target="_self">
                <button style="padding:6px 12px;">Open</button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
