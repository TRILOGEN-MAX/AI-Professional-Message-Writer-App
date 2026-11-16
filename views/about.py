"""
About Page for BlackHole AI.
Overview of features, architecture, technology stack, and developer credits.
"""

import streamlit as st
from components.ui_components import render_logo, render_hero_badge


def render_about_page():
    """Render the application about and architecture details."""
    st.markdown(render_hero_badge("Enterprise-Grade Career Communications"), unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.3rem;">
            About <span class="bh-glow-text">BlackHole AI</span>
        </h2>
        <p class="bh-sub-text">
            Gravitational intelligence designed to cut through recruiter inbox noise with maximum impact.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Mission Statement Card
    st.markdown('<div class="bh-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color: #f8fafc;">
        Our Mission
    </h3>
    <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">
        Job hunting as a student, fresh graduate, or career transitioner is often exhausting. Cold emails get 
        lost in spam, and LinkedIn connection requests are skipped because they sound robotic or fail character limits. 
        <strong>BlackHole AI</strong> solves this by using state-of-the-art Google Gemini models to synthesize 
        your genuine achievements into respectful, highly articulate, and conversion-optimized career correspondence.
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Architecture & Technology Stack Card
    st.markdown('<div class="bh-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem; color: #f8fafc;">
        Technology Architecture
    </h3>
    """, unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    with t1:
        st.markdown("""
        - **Frontend Framework:** Streamlit (Python 3.10+ / 3.14)
        - **AI Foundation:** Google Gemini Models (`gemini-3.5-flash`)
        - **SDK:** Official `google-genai` Python SDK
        - **Design System:** Custom CSS & Deep Space Glassmorphism
        """)
    with t2:
        st.markdown("""
        - **Data Persistence:** SQLite3 (Local, Encrypted at OS-level)
        - **Environment Security:** `python-dotenv` & Streamlit Secrets
        - **Constraints Engine:** Client-side & Model-level character enforcement
        - **Clipboard Architecture:** Browser-safe API with native fallback
        """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Core Features Summary
    st.markdown('<div class="bh-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem; color: #f8fafc;">
        Core Capabilities
    </h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div>
            <div style="color: #c084fc; font-weight: 600; font-size: 0.95rem;">✉️ Multi-Role Email Generation</div>
            <div style="color: #94a3b8; font-size: 0.85rem;">Distinct phrasing optimized for HR, Recruiters, Professors, and Hiring Managers with auto-generated subjects.</div>
        </div>
        <div>
            <div style="color: #38bdf8; font-weight: 600; font-size: 0.95rem;">🔗 Strict 300-Char LinkedIn Enforcer</div>
            <div style="color: #94a3b8; font-size: 0.85rem;">Guarantees notes fit within LinkedIn's connection request modal without being cut off.</div>
        </div>
        <div>
            <div style="color: #a855f7; font-weight: 600; font-size: 0.95rem;">🔄 Intelligent Regeneration</div>
            <div style="color: #94a3b8; font-size: 0.85rem;">Explores distinct narrative angles without hallucinating or losing core facts.</div>
        </div>
        <div>
            <div style="color: #4ade80; font-weight: 600; font-size: 0.95rem;">🔒 Zero Data Leakage</div>
            <div style="color: #94a3b8; font-size: 0.85rem;">Local SQLite storage ensures zero telemetry or third-party tracking.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Developer Information
    st.markdown('<div class="bh-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color: #f8fafc;">
        Engineering & Credits
    </h3>
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
        <div>
            <div style="font-weight: 600; color: #f8fafc;">Architect & Developer: <span style="color: #c084fc;">BlackHole AI Core Team</span></div>
            <div style="color: #94a3b8; font-size: 0.85rem;">Role: Full-Stack AI Engineer & UI/UX Designer</div>
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #64748b;">
            Version: 1.0.0-PROD &bull; Release: 2026.11
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Back to Dashboard button
    if st.button("⬅️ Return to Dashboard", key="btn_about_return_home"):
        st.session_state["current_page"] = "Home"
        st.rerun()
