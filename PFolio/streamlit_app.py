import streamlit as st

# ---------- BASIC CONFIG ----------

st.set_page_config(
    page_title="Anil Vasudevakurup | Product Management Portfolio",
    page_icon="💼",
    layout="wide"
)

# ---------- HEADER SECTION ----------

NAME = "Anil Vasudevakurup"
ROLE = "Director of Product Management | SaaS, AI, Field Service, ERP Integrations | Customer Success Leader"
LOCATION = "Denver, CO"
EMAIL = "your.email@example.com"  # TODO: update with real email
LINKEDIN_URL = "https://www.linkedin.com/in/anil-vasudevakurup/"

# Optional headshot path in assets/
HEADSHOT_PATH = "assets/anil_headshot.jpg"  # put your image there or comment out


def main():
    # Top area: name + summary
    cols = st.columns([1, 3])

    with cols[0]:
        try:
            st.image(HEADSHOT_PATH, use_container_width=True)
        except Exception:
            st.write("")  # no image yet

    with cols[1]:
        st.title(NAME)
        st.write(ROLE)
        st.markdown(
            f"**{LOCATION}**  •  📧 `{EMAIL}`  •  "
            f"[LinkedIn]({LINKEDIN_URL})"
        )

    st.divider()

    # ---------- ABOUT ME ----------
    st.subheader("About Me")

    st.markdown(
        """
I am a strategic product executive who builds intelligent, scalable solutions at the intersection of **AI, Field Service, Digital Commerce, and Cloud SaaS**. Over the past 15+ years, I’ve guided global teams and complex enterprise programs across Oracle, HP, and high-growth SaaS environments—transforming ambiguity into strategy, and strategy into measurable business outcomes.

My work sits at the core of how organizations operate. I’ve led the design and delivery of cloud-native products that streamline field service operations, modernize B2B eCommerce, and integrate seamlessly with ERP ecosystems such as **Infor, Karmak, SAP, and DST**. I understand how data, workflow automation, and customer experience come together to create meaningful competitive advantage.

With hands-on expertise in **Oracle Field Service (OFS/OFSC)**, AI-driven automation, and **AWS/Azure** integration, I specialize in turning complex operational and technical landscapes into intuitive, high-performing products. My teams and I have delivered results that matter—**40% efficiency improvements**, **double-digit revenue acceleration**, and **retention rates above 80%** by staying grounded in customer needs and aligned with business strategy.

What I enjoy most is building clarity, collaboration, and momentum across engineering, design, sales, and customer success. I lead with empathy, analytical rigor, and a bias for action, ensuring that every product decision moves the business forward while enabling teams to perform at their highest level.

I am driven by the belief that great products don’t just solve problems—they **elevate organizations, empower users, and create long-term value**. That is the mindset I bring to every role, every customer, and every product I help shape.
        """
    )

    st.divider()

    # ---------- QUICK LINKS ----------
    st.subheader("Portfolio Links")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.link_button("🔗 LinkedIn", LINKEDIN_URL)
    with c2:
        st.link_button("📄 Download Resume", "#", help="Replace '#' with resume URL")
    with c3:
        st.link_button("📂 Product Portfolio", "https://avasudev18.github.io/PFolioAV.github.io/index.html")

    st.divider()

    # ---------- CORE EXPERTISE ----------
    st.subheader("Core Expertise")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
### Product Leadership
- Product strategy & vision  
- Roadmapping & prioritization frameworks  
- Go-to-market strategy  
- Cross-functional alignment  
- Stakeholder influence & executive communication  

### AI / Machine Learning
- AI agents & generative AI workflows  
- RAG pipelines & knowledge retrieval  
- Recommendation models & catalog intelligence  
- Predictive analytics & forecasting  
            """
        )

    with col2:
        st.markdown(
            """
### Enterprise Systems
- Oracle Field Service & Oracle Cloud  
- Infor, Karmak, DST & ERP commerce workflows  
- Large-scale integrations across eCommerce and field service  

### Customer Success Leadership
- Adoption & onboarding workflows  
- Retention & renewal strategy  
- NPS improvement & support optimization  
- KPI-driven engagement models (NRR, GRR, CSAT, SLA)

### Tools & Platforms
- Gemini, ChatGPT, Claude, NoteLM, Gamma  
- Jira, Figma, Python, Kaggle  
- Oracle Cloud Infrastructure (OCI), AWS, Azure, GCP  
            """
        )

    st.info(
        "Use the **sidebar navigation** to explore live implementations, customer success leadership, "
        "thought-leadership projects, and detailed experience & education."
    )


if __name__ == "__main__":
    main()

