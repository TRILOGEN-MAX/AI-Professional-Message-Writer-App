"""
Home / Dashboard Page for BlackHole AI.
"""

import streamlit as st
from components.ui_components import render_hero_badge, render_feature_card, render_black_hole_visual
from services.history_service import get_history_stats


def render_home_page():
    """Render the landing dashboard."""
    # Top Hero Badge
    st.markdown(render_hero_badge("Cosmic Career Acceleration &bull; Powered by Gemini 3.5 Flash"), unsafe_allow_html=True)

    # Hero Headline and Subtitle
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-size: 2.8rem; font-weight: 800; line-height: 1.15; margin-bottom: 0.8rem;">
            Your Words. Your Opportunities. <br/>
            <span class="bh-glow-text">Powered by AI.</span>
        </h1>
        <p class="bh-sub-text" style="max-width: 780px;">
            BlackHole AI empowers students, graduates, and professionals to generate irresistible, 
            high-converting cold emails and LinkedIn messages for dream jobs, coveted internships, 
            and career-defining referrals.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Hero CTA Buttons
    col_btn1, col_btn2, col_spacer = st.columns([1.5, 1.5, 3])
    with col_btn1:
        if st.button("🚀 Create a Message", key="hero_btn_create", use_container_width=True):
            st.session_state["current_page"] = "Create Message"
            st.rerun()

    with col_btn2:
        if st.button("🌌 Explore Features", key="hero_btn_features", use_container_width=True, type="secondary"):
            st.session_state["scroll_to_features"] = True
            st.toast("Explore our 3 core message modules below!", icon="✨")

    # Black Hole Event Horizon Visual Centerpiece
    st.markdown(render_black_hole_visual(), unsafe_allow_html=True)

    # Real-Time Statistics Row
    stats = get_history_stats()
    st.markdown("""
    <div style="font-size: 0.85rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 0.75rem;">
        Activity Horizon
    </div>
    """, unsafe_allow_html=True)

    stat1, stat2, stat3 = st.columns(3)
    with stat1:
        st.markdown(f"""
        <div class="bh-stat-card">
            <div class="bh-stat-val">{stats['total_messages']}</div>
            <div class="bh-stat-lbl">Total Messages Generated</div>
        </div>
        """, unsafe_allow_html=True)

    with stat2:
        st.markdown(f"""
        <div class="bh-stat-card">
            <div class="bh-stat-val">{stats['email_messages']}</div>
            <div class="bh-stat-lbl">Emails Crafted</div>
        </div>
        """, unsafe_allow_html=True)

    with stat3:
        st.markdown(f"""
        <div class="bh-stat-card">
            <div class="bh-stat-val">{stats['linkedin_messages']}</div>
            <div class="bh-stat-lbl">LinkedIn Notes (300 Chars)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Three Core Feature Cards
    st.markdown("""
    <div style="font-size: 0.85rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 0.75rem;">
        Core Generation Engines
    </div>
    """, unsafe_allow_html=True)

    col_feat1, col_feat2, col_feat3 = st.columns(3)
    with col_feat1:
        st.markdown(render_feature_card(
            title="1. Professional Email Generator",
            description="Craft magnetic subject lines and articulate email bodies tailored for HR, recruiters, professors, and executive hiring leads.",
            tag="Full Suite",
            icon="✉️"
        ), unsafe_allow_html=True)
        if st.button("Launch Email Mode", key="feat_launch_email", use_container_width=True):
            st.session_state["default_platform_override"] = "Email"
            st.session_state["current_page"] = "Create Message"
            st.rerun()

    with col_feat2:
        st.markdown(render_feature_card(
            title="2. LinkedIn Note Generator",
            description="Strictly enforced &le; 300 character connection notes and InMails that break through the noise without being truncated.",
            tag="Strict 300 Chars",
            icon="🔗"
        ), unsafe_allow_html=True)
        if st.button("Launch LinkedIn Mode", key="feat_launch_linkedin", use_container_width=True):
            st.session_state["default_platform_override"] = "LinkedIn"
            st.session_state["current_page"] = "Create Message"
            st.rerun()

    with col_feat3:
        st.markdown(render_feature_card(
            title="3. AI-Powered Regeneration",
            description="Intelligently spins fresh variations and hooks from your core points while maintaining tone, truthfulness, and structure.",
            tag="Zero Duplication",
            icon="🔄"
        ), unsafe_allow_html=True)
        if st.button("Explore History", key="feat_launch_regen", use_container_width=True):
            st.session_state["current_page"] = "Message History"
            st.rerun()

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Recent Message Activity Section
    st.markdown("""
    <div style="font-size: 0.85rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 0.75rem;">
        Recent Space Missions (Recent Activity)
    </div>
    """, unsafe_allow_html=True)

    if stats["recent_activity"]:
        st.markdown('<div class="bh-card" style="padding: 1rem;">', unsafe_allow_html=True)
        for act in stats["recent_activity"]:
            badge_icon = "🔗" if act["platform"] == "LinkedIn" else "✉️"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(139, 92, 246, 0.1);">
                <div>
                    <span style="font-weight: 600; color: #f8fafc;">{badge_icon} {act['platform']}</span>
                    <span style="color: #94a3b8; font-size: 0.85rem; margin-left: 10px;">{act['message_type']}</span>
                </div>
                <div style="color: #64748b; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace;">
                    {act['created_at']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No messages generated yet. Jump into 'Create Message' to launch your first opportunity!")
