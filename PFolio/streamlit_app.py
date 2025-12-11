import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Anil Vasudevakurup | Product Management Portfolio",
    page_icon="💼",
    layout="wide"
)

NAME = "Anil Vasudevakurup"
ROLE = "Director of Product Management | SaaS, AI, Field Service, ERP Integrations | Customer Success Leader"
LOCATION = "Denver, CO"
EMAIL = "your.email@example.com"
LINKEDIN_URL = "https://www.linkedin.com/in/anil-vasudevakurup/"

HEADSHOT_PATH = Path("assets/anil_headshot.jpg")  # local image


def main():
    cols = st.columns([1, 3])

    with cols[0]:
        if HEADSHOT_PATH.is_file():
            st.image(str(HEADSHOT_PATH), use_container_width=True)
        else:
            # Simple fallback so you see *something*
            st.markdown(
                """
                <div style="font-size:60px; text-align:center;">👤</div>
                <p style="text-align:center; color:gray;">Upload assets/anil_headshot.jpg</p>
                """,
                unsafe_allow_html=True,
            )

    with cols[1]:
        st.title(NAME)
        st.write(ROLE)
        st.markdown(
            f"**{LOCATION}** • 📧 `{EMAIL}` • [LinkedIn]({LINKEDIN_URL})"
        )

    st.divider()

    # ... (rest of your existing Home page code here) ...


if __name__ == "__main__":
    main()
