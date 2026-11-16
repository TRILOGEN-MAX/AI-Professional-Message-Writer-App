"""
Message History Page for BlackHole AI.
Allows viewing, copying, deleting individual records, or clearing entire history.
"""

import streamlit as st
import html
from services.history_service import get_all_messages, delete_message, clear_all_history


def render_history_page():
    """Render the message archive and history manager."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.3rem;">
            Message History <span class="bh-glow-text">&bull; Archive</span>
        </h2>
        <p class="bh-sub-text">
            Persistent local record of all drafted communications. Revisit, copy, or purge records anytime.
        </p>
    </div>
    """, unsafe_allow_html=True)

    messages = get_all_messages()

    # Top Control Bar
    top_col1, top_col2 = st.columns([3, 1.2])
    with top_col1:
        st.markdown(f"""
        <div style="font-size: 0.95rem; color: #94a3b8; padding-top: 0.5rem;">
            Showing <strong>{len(messages)}</strong> saved communication missions.
        </div>
        """, unsafe_allow_html=True)

    with top_col2:
        if messages:
            if st.button("🗑️ Clear All History", key="btn_clear_all_history_prompt", use_container_width=True, type="secondary"):
                st.session_state["confirm_clear_all"] = True

    # Confirmation Dialog for Clear All
    if st.session_state.get("confirm_clear_all", False):
        st.warning("⚠️ Are you sure you want to permanently delete all message records?")
        c_yes, c_no, _ = st.columns([1, 1, 3])
        with c_yes:
            if st.button("Yes, Clear Everything", key="btn_confirm_clear_yes", type="primary"):
                clear_all_history()
                st.session_state["confirm_clear_all"] = False
                st.toast("🧹 All message history has been wiped.", icon="✨")
                st.rerun()
        with c_no:
            if st.button("Cancel", key="btn_confirm_clear_no"):
                st.session_state["confirm_clear_all"] = False
                st.rerun()

    if not messages:
        st.markdown("""
        <div class="bh-card" style="text-align: center; padding: 3rem 1.5rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌌</div>
            <h3 style="font-size: 1.3rem; margin-bottom: 0.5rem; color: #f8fafc;">Your Archive is Empty</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; max-width: 500px; margin: 0 auto 1.5rem auto;">
                No communications have been saved yet. Use the Message Generator to draft your next career outreach.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Jump to Message Generator", key="btn_history_to_gen", use_container_width=False):
            st.session_state["current_page"] = "Create Message"
            st.rerun()
        return

    # List Saved Messages
    for msg in messages:
        msg_id = msg["id"]
        is_linkedin = msg["platform"] == "LinkedIn"
        icon = "🔗" if is_linkedin else "✉️"
        badge_cls = "bh-badge-cyan" if is_linkedin else ""

        with st.expander(
            f"{icon} [{msg['platform']}] {msg['message_type']} - To: {msg['recipient_name'] or msg['recipient']} ({msg['created_at'][:16]})",
            expanded=False
        ):
            st.markdown('<div style="padding: 0.5rem 0;">', unsafe_allow_html=True)

            # Metadata header
            st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 0.8rem; font-size: 0.82rem;">
                <span class="bh-badge {badge_cls}">{msg['platform']}</span>
                <span style="color: #94a3b8;">Type: <strong style="color: #f8fafc;">{msg['message_type']}</strong></span>
                <span style="color: #94a3b8;">Recipient: <strong style="color: #f8fafc;">{msg['recipient_name'] or msg['recipient']}</strong></span>
                <span style="color: #94a3b8;">Tone: <strong style="color: #c084fc;">{msg['tone']}</strong></span>
                <span style="color: #94a3b8;">Length: <strong style="color: #38bdf8;">{msg['char_count']} chars</strong></span>
            </div>
            """, unsafe_allow_html=True)

            # Subject Line if exists
            if msg.get("subject"):
                st.markdown(f"""
                <div style="margin-bottom: 0.75rem;">
                    <div style="font-size: 0.75rem; text-transform: uppercase; color: #94a3b8; font-weight: 600;">Subject:</div>
                    <div style="font-weight: 600; color: #f8fafc; font-size: 0.95rem; background: rgba(18, 18, 30, 0.6); padding: 0.5rem 0.75rem; border-radius: 6px; border: 1px solid rgba(139, 92, 246, 0.2);">
                        {html.escape(msg['subject'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Message content box
            st.markdown("""
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #94a3b8; font-weight: 600; margin-bottom: 0.25rem;">Content:</div>
            """, unsafe_allow_html=True)
            st.text_area(
                label=f"Content #{msg_id}",
                value=msg["content"],
                height=140 if is_linkedin else 200,
                key=f"hist_txt_{msg_id}",
                label_visibility="collapsed"
            )

            # Action Buttons Row
            b_col1, b_col2, b_col3, b_spacer = st.columns([1.2, 1.2, 1.2, 2.5])

            with b_col1:
                if st.button("📋 Copy Text", key=f"hist_copy_{msg_id}", use_container_width=True):
                    st.code(msg["content"], language=None)
                    st.toast("✅ Copied to clipboard codeblock above!", icon="📋")

            with b_col2:
                if msg.get("subject"):
                    if st.button("📑 Copy Subject", key=f"hist_sub_{msg_id}", use_container_width=True):
                        st.code(msg["subject"], language=None)
                        st.toast("✅ Subject copied!", icon="📑")
                else:
                    if st.button("⚡ Open in Generator", key=f"hist_load_{msg_id}", use_container_width=True):
                        st.session_state["last_result"] = {
                            "success": True,
                            "platform": msg["platform"],
                            "subject": msg["subject"],
                            "content": msg["content"],
                            "char_count": msg["char_count"]
                        }
                        st.session_state["last_inputs"] = {
                            "platform": msg["platform"],
                            "message_type": msg["message_type"],
                            "recipient": msg["recipient"],
                            "recipient_name": msg["recipient_name"],
                            "tone": msg["tone"],
                            "key_points": msg.get("key_points", ""),
                            "additional_context": msg.get("additional_context", "")
                        }
                        st.session_state["current_page"] = "Create Message"
                        st.rerun()

            with b_col3:
                if st.button("🗑️ Delete", key=f"hist_del_{msg_id}", use_container_width=True, type="secondary"):
                    delete_message(msg_id)
                    st.toast(f"Record #{msg_id} deleted.", icon="🗑️")
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
