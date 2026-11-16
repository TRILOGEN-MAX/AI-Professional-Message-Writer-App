"""
Settings Page for BlackHole AI.
Allows checking API connection status, instructions for secure setup,
configuring preferences (default tone and platform), and data management.
"""

import streamlit as st
import os
from services.gemini_service import is_api_key_configured, get_api_key
from services.history_service import clear_all_history, get_history_stats


def render_settings_page():
    """Render application settings and engine status."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.3rem;">
            System Settings <span class="bh-glow-text">&bull; Core Control</span>
        </h2>
        <p class="bh-sub-text">
            Manage your Gemini AI integration, generation defaults, and workspace data privacy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. AI Engine Status Card
    st.markdown('<div class="bh-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.5rem; color: #f8fafc;">
        Google Gemini AI Status
    </div>
    """, unsafe_allow_html=True)

    api_configured = is_api_key_configured()

    if api_configured:
        key_val = get_api_key() or ""
        masked_key = f"{key_val[:4]}...{key_val[-4:]}" if len(key_val) > 8 else "Active &bull;&bull;&bull;&bull;"
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 8px; padding: 0.75rem 1rem;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.2rem;">🟢</span>
                <div>
                    <div style="font-weight: 600; color: #86efac; font-size: 0.92rem;">Gemini Engine Connected</div>
                    <div style="color: #94a3b8; font-size: 0.78rem;">Key: {masked_key}</div>
                </div>
            </div>
            <span class="bh-badge bh-badge-green">Operational</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 0.75rem 1rem;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.2rem;">🔴</span>
                <div>
                    <div style="font-weight: 600; color: #fca5a5; font-size: 0.92rem;">API Key Not Detected</div>
                    <div style="color: #94a3b8; font-size: 0.78rem;">Configure GEMINI_API_KEY in environment or below.</div>
                </div>
            </div>
            <span class="bh-badge" style="background: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #fca5a5;">Disconnected</span>
        </div>
        """, unsafe_allow_html=True)

    # Session Key Configuration Box (Safe runtime injection without disk exposure)
    st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.85rem; font-weight: 600; color: #f8fafc; margin-bottom: 0.4rem;">
        Runtime Session API Key Override
    </div>
    <div style="font-size: 0.78rem; color: #94a3b8; margin-bottom: 0.5rem;">
        You can supply an API key for the current session without saving it to disk:
    </div>
    """, unsafe_allow_html=True)

    col_k1, col_k2 = st.columns([3, 1])
    with col_k1:
        session_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            label_visibility="collapsed"
        )
    with col_k2:
        if st.button("Apply Key", key="btn_apply_session_key", use_container_width=True):
            if session_key_input.strip():
                os.environ["GEMINI_API_KEY"] = session_key_input.strip()
                st.toast("✅ Session API key configured successfully!", icon="🔑")
                st.rerun()
            else:
                st.error("Please enter a valid key string.")

    # Instructions Expander
    with st.expander("📖 Instructions for Permanent Gemini API Setup", expanded=False):
        st.markdown("""
        **Method A: Using `.env` file (Recommended for local dev)**
        1. Open or create `.env` in the root folder of this project.
        2. Add the following line:
           ```bash
           GEMINI_API_KEY=your_actual_gemini_api_key_here
           ```
        3. Save the file. BlackHole AI will automatically load it.

        **Method B: Streamlit Secrets (For Streamlit Cloud / Hosting)**
        1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`.
        2. Set:
           ```toml
           GEMINI_API_KEY = "your_actual_gemini_api_key_here"
           ```

        **Where do I get a free API Key?**
        - Visit [Google AI Studio](https://aistudio.google.com/)
        - Sign in with your Google Account and click **"Get API key"**.
        """)

    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Generation Preferences Card
    st.markdown('<div class="bh-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.5rem; color: #f8fafc;">
        Generation Defaults
    </div>
    <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;">
        Set default selections when opening the message creation engine.
    </p>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        current_default_platform = st.session_state.get("setting_default_platform", "Email")
        new_platform = st.selectbox(
            "Preferred Default Platform",
            options=["Email", "LinkedIn"],
            index=0 if current_default_platform == "Email" else 1,
            key="set_def_platform"
        )

    with col_p2:
        current_default_tone = st.session_state.get("setting_default_tone", "Professional")
        tones = ["Professional", "Friendly", "Formal", "Confident", "Concise"]
        tone_idx = tones.index(current_default_tone) if current_default_tone in tones else 0
        new_tone = st.selectbox(
            "Preferred Default Tone",
            options=tones,
            index=tone_idx,
            key="set_def_tone"
        )

    if st.button("💾 Save Preferences", key="btn_save_preferences"):
        st.session_state["setting_default_platform"] = new_platform
        st.session_state["setting_default_tone"] = new_tone
        st.toast("✅ Preferences saved successfully!", icon="💾")

    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Data & Privacy Management Card
    st.markdown('<div class="bh-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.5rem; color: #f8fafc;">
        Data Privacy & Local Storage
    </div>
    <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;">
        All generated drafts and input logs are preserved entirely inside your local SQLite database (<code>database/history.db</code>).
        No user messages or credentials are ever shared or transmitted to 3rd party databases.
    </p>
    """, unsafe_allow_html=True)

    stats = get_history_stats()
    st.markdown(f"""
    <div style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 1rem;">
        Currently tracking <strong>{stats['total_messages']}</strong> message records on disk.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Purge Local Database History", key="btn_settings_purge_hist", type="secondary"):
        st.session_state["confirm_settings_purge"] = True

    if st.session_state.get("confirm_settings_purge", False):
        st.warning("⚠️ This action will permanently remove all saved message history.")
        col_py, col_pn = st.columns([1, 1])
        with col_py:
            if st.button("Confirm Purge", key="btn_confirm_purge_yes", type="primary"):
                clear_all_history()
                st.session_state["confirm_settings_purge"] = False
                st.toast("🧹 Local database history successfully cleared.", icon="✨")
                st.rerun()
        with col_pn:
            if st.button("Cancel", key="btn_confirm_purge_no"):
                st.session_state["confirm_settings_purge"] = False
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
