"""
Message Card Component for displaying generated results with full actions:
Copy, Regenerate, Save, Clear.
"""

import streamlit as st
import html
from services.history_service import save_message


def render_message_result_card(
    platform: str,
    content: str,
    subject: str = None,
    char_count: int = 0,
    metadata: dict = None,
    on_regenerate_callback=None
):
    """
    Renders the result card with Subject, Body, Character Counters,
    and action buttons (Copy Subject, Copy Message, Regenerate, Save, Clear).
    """
    if metadata is None:
        metadata = {}

    st.markdown('<div class="bh-card">', unsafe_allow_html=True)

    # Header with platform and character badge
    is_linkedin = platform == "LinkedIn"
    limit_badge = ""
    if is_linkedin:
        safe_class = "bh-counter-safe" if char_count <= 300 else "bh-counter-danger"
        limit_badge = f'<span class="bh-counter {safe_class}">{char_count} / 300 chars</span>'
    else:
        limit_badge = f'<span class="bh-counter bh-counter-safe">{char_count} characters</span>'

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid rgba(139, 92, 246, 0.2); padding-bottom: 0.75rem;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="bh-badge {'bh-badge-cyan' if is_linkedin else ''}">
                {'🔗 ' if is_linkedin else '✉️ '} {platform.upper()} DRAFT
            </span>
            <span style="font-size: 0.85rem; color: #94a3b8;">
                Tone: <strong style="color: #c084fc;">{metadata.get('tone', 'Professional')}</strong>
            </span>
        </div>
        <div>
            {limit_badge}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Subject line display for Email
    if not is_linkedin and subject:
        st.markdown(f"""
        <div style="margin-bottom: 1.25rem;">
            <div style="font-size: 0.85rem; text-transform: uppercase; color: #c084fc; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 6px;">
                <span>📌</span> Subject Line
            </div>
            <div style="background: rgba(18, 18, 32, 0.95); border: 1.5px solid rgba(168, 85, 247, 0.45); border-radius: 12px; padding: 1rem 1.25rem; font-weight: 600; color: #ffffff; font-size: 1.15rem; line-height: 1.5; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);">
                {html.escape(subject)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Message Content display label
    st.markdown("""
    <div style="font-size: 0.85rem; text-transform: uppercase; color: #38bdf8; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 6px;">
        <span>📝</span> Generated Message Body
    </div>
    """, unsafe_allow_html=True)

    # Large, spacious, highly readable message text area
    st.text_area(
        label="Message Content",
        value=content,
        height=240 if is_linkedin else 450,
        key="active_generated_text_area",
        label_visibility="collapsed"
    )

    # Action Buttons Bar
    st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 1.1, 1.1, 1.0])

    with col1:
        # Copy Message
        if st.button("📋 Copy Message", key="btn_copy_msg", use_container_width=True):
            st.code(content, language=None)
            st.toast("✅ Message ready! Copied above for instant clipboard access.", icon="📋")

    with col2:
        # Copy Subject (Email only) or character check (LinkedIn)
        if not is_linkedin and subject:
            if st.button("📑 Copy Subject", key="btn_copy_subj", use_container_width=True):
                st.code(subject, language=None)
                st.toast("✅ Subject line ready above!", icon="📑")
        else:
            if st.button("🔍 Check Limit", key="btn_check_limit", use_container_width=True):
                if char_count <= 300:
                    st.toast(f"✅ Compliant! {char_count}/300 chars.", icon="✨")
                else:
                    st.toast(f"⚠️ Over limit by {char_count - 300} chars!", icon="⚠️")

    with col3:
        # Regenerate
        if st.button("🔄 Regenerate", key="btn_regen", use_container_width=True):
            if on_regenerate_callback:
                on_regenerate_callback()

    with col4:
        # Save to History
        if st.button("💾 Save to History", key="btn_save_hist", use_container_width=True):
            saved_id = save_message(
                platform=platform,
                message_type=metadata.get("message_type", "Job Application"),
                recipient=metadata.get("recipient", "HR Manager"),
                recipient_name=metadata.get("recipient_name", ""),
                tone=metadata.get("tone", "Professional"),
                content=content,
                subject=subject,
                key_points=metadata.get("key_points", ""),
                additional_context=metadata.get("additional_context", "")
            )
            st.toast(f"🎉 Message saved to History (ID #{saved_id})!", icon="💾")

    with col5:
        # Clear Result
        if st.button("🗑️ Clear", key="btn_clear_res", use_container_width=True, type="secondary"):
            if "last_result" in st.session_state:
                del st.session_state["last_result"]
            st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)
