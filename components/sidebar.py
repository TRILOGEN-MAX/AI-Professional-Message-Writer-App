"""
Custom Sidebar navigation component for BlackHole AI.
Provides clean status indicators, active links, and brand visuals.
"""

import streamlit as st
from components.ui_components import render_logo
from services.gemini_service import is_api_key_configured
from services.history_service import get_history_stats


def render_sidebar():
    """Render application sidebar with brand identity, quick stats and status."""
    with st.sidebar:
        st.markdown(render_logo(42), unsafe_allow_html=True)

        st.markdown("""
        <div style="margin: 0.5rem 0 1.5rem 0; font-size: 0.8rem; color: #94a3b8; line-height: 1.4;">
            Next-gen gravitational communication engine for job seekers & scholars.
        </div>
        """, unsafe_allow_html=True)

        # Navigation links with active highlighting
        st.markdown("""
        <div style="font-size: 0.72rem; text-transform: uppercase; color: #64748b; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 0.75rem;">
            Navigation Hub
        </div>
        """, unsafe_allow_html=True)

        pages = [
            ("Home", "🏠 Home", "home"),
            ("Create Message", "⚡ Create Message", "generator"),
            ("Message History", "📁 Message History", "history"),
            ("Settings", "⚙️ Settings", "settings"),
            ("About", "🌌 About", "about"),
        ]

        current_page = st.session_state.get("current_page", "Home")

        for page_name, label, icon_id in pages:
            is_active = (current_page == page_name)
            button_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_{icon_id}", use_container_width=True, type=button_type):
                st.session_state["current_page"] = page_name
                st.rerun()

        st.markdown("<hr style='border-color: rgba(139, 92, 246, 0.15); margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # System Status Widget
        api_ok = is_api_key_configured()
        status_color = "#4ade80" if api_ok else "#f87171"
        status_text = "Gemini Engine Connected" if api_ok else "API Key Not Set"
        status_sub = "Ready to generate" if api_ok else "Configure in Settings"

        st.markdown(f"""
        <div style="background: rgba(14, 14, 26, 0.7); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 10px; padding: 0.85rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:{status_color}; box-shadow: 0 0 8px {status_color};"></span>
                <span style="font-size: 0.82rem; font-weight: 600; color: #f8fafc;">{status_text}</span>
            </div>
            <div style="font-size: 0.72rem; color: #94a3b8; margin-left: 16px;">
                {status_sub}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick stats
        stats = get_history_stats()
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8; padding: 0.25rem 0.5rem;">
            <span>Saved Messages:</span>
            <strong style="color: #c084fc;">{stats['total_messages']}</strong>
        </div>
        <div style="text-align: center; margin-top: 1.5rem; font-size: 0.7rem; color: #64748b;">
            BlackHole AI &bull; v1.0.0
        </div>
        """, unsafe_allow_html=True)
