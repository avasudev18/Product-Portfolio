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

    # … keep the rest of your home-page content unchanged …
    # (Quick links, Core Expertise, etc.)


if __name__ == "__main__":
    main()
