"""
Message Generator Page for BlackHole AI.
Interactive form for Email and LinkedIn message generation with full Gemini AI integration.
"""

import streamlit as st
import random
from services.gemini_service import generate_message, is_api_key_configured
from services.history_service import save_message
from components.message_card import render_message_result_card


def render_generator_page():
    """Render the main message creation engine."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.3rem;">
            Message Generator <span class="bh-glow-text">&bull; Core</span>
        </h2>
        <p class="bh-sub-text">
            Configure your target opportunity and let BlackHole AI gravitational intelligence architect your note.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Check API key status
    api_ready = is_api_key_configured()
    if not api_ready:
        st.warning(
            "⚠️ **Gemini API Key is not detected.** You can configure it in the **Settings** page or add `GEMINI_API_KEY` to `.env`. "
            "Until configured, test generation will prompt for setup."
        )

    # Defaults from settings or overrides
    default_platform = st.session_state.get("default_platform_override") or st.session_state.get("setting_default_platform", "Email")
    default_tone = st.session_state.get("setting_default_tone", "Professional")

    # Clear platform override after loading
    if "default_platform_override" in st.session_state:
        del st.session_state["default_platform_override"]

    # --- INPUT FORM CARD ---
    st.markdown('<div class="bh-card">', unsafe_allow_html=True)

    col_plat, col_type = st.columns(2)
    with col_plat:
        platform_options = ["Email", "LinkedIn"]
        selected_platform = st.selectbox(
            "Target Platform *",
            options=platform_options,
            index=0 if default_platform == "Email" else 1,
            help="LinkedIn enforces a strict 300 character limit. Email crafts full professional subject & body."
        )

    with col_type:
        type_options = [
            "Job Application",
            "Referral Request",
            "Interview Follow-up",
            "Internship Request",
            "Thank You After Interview"
        ]
        selected_type = st.selectbox(
            "Message Type *",
            options=type_options,
            index=0,
            help="The primary objective of your communication."
        )

    col_recip, col_name, col_tone = st.columns([1.2, 1.2, 1.1])
    with col_recip:
        recipient_options = [
            "HR Manager",
            "Recruiter",
            "Professor",
            "Hiring Manager",
            "Employee",
            "Other"
        ]
        selected_recipient = st.selectbox("Recipient Category *", options=recipient_options, index=0)

    with col_name:
        recipient_name = st.text_input(
            "Recipient Name (Optional)",
            placeholder="e.g. Dr. Aris Thorne or Sarah Jenkins",
            help="Leave blank if unknown; suitable professional placeholders or generic titles will be used."
        )

    with col_tone:
        tone_options = ["Professional", "Friendly", "Formal", "Confident", "Concise"]
        tone_index = tone_options.index(default_tone) if default_tone in tone_options else 0
        selected_tone = st.selectbox("Desired Tone *", options=tone_options, index=tone_index)

    # Key Points Multiline Area
    key_points = st.text_area(
        "Key Points to Include * (2–3 important highlights)",
        placeholder="1. 2 years experience in React and Python\n2. Built an open-source tool with 500+ stars\n3. Eager to contribute to the upcoming cloud platform launch",
        height=120,
        help="Specify the real facts, achievements, or requirements you want highlighted. AI will not fabricate unmentioned skills."
    )

    # Additional Context
    additional_context = st.text_area(
        "Additional Context (Optional)",
        placeholder="Job Title: Senior Backend Engineer | Company: Stellar Dynamics | Mention that we met at the PyCon 2026 conference",
        height=80,
        help="Add job title, company name, mutual connections, or background details."
    )

    # Pre-generation interactive character hint for LinkedIn
    if selected_platform == "LinkedIn":
        st.markdown("""
        <div style="margin-bottom: 0.8rem; font-size: 0.82rem; color: #38bdf8; display: flex; align-items: center; gap: 6px;">
            <span>ℹ️</span> <strong>LinkedIn Mode Active:</strong> Output will be strictly optimized and verified under 300 characters.
        </div>
        """, unsafe_allow_html=True)

    # Generation Button
    btn_generate = st.button("✨ Generate with BlackHole AI", key="btn_execute_generate", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Handle Generation
    if btn_generate:
        # Validation
        if not key_points.strip():
            st.error("❌ Please provide at least 1–2 Key Points to include in your message.")
            return

        with st.spinner("🌌 Collapsing noise... Synthesizing gravitational message with Gemini..."):
            result = generate_message(
                platform=selected_platform,
                message_type=selected_type,
                recipient=selected_recipient,
                recipient_name=recipient_name.strip() if recipient_name else None,
                tone=selected_tone,
                key_points=key_points.strip(),
                additional_context=additional_context.strip() if additional_context else None
            )

        if result.get("success"):
            # Auto-save to session state
            st.session_state["last_result"] = result
            st.session_state["last_inputs"] = {
                "platform": selected_platform,
                "message_type": selected_type,
                "recipient": selected_recipient,
                "recipient_name": recipient_name.strip() if recipient_name else None,
                "tone": selected_tone,
                "key_points": key_points.strip(),
                "additional_context": additional_context.strip() if additional_context else None,
                "regen_count": 0
            }
            # Also auto-save to persistent history for user convenience
            save_message(
                platform=selected_platform,
                message_type=selected_type,
                recipient=selected_recipient,
                recipient_name=recipient_name.strip() if recipient_name else None,
                tone=selected_tone,
                content=result["content"],
                subject=result.get("subject"),
                key_points=key_points.strip(),
                additional_context=additional_context.strip() if additional_context else None
            )
            st.rerun()
        else:
            if result.get("error_type") == "MISSING_KEY":
                st.error(f"❌ {result.get('error')}")
                if st.button("Go to Settings to add API Key", key="btn_err_go_settings"):
                    st.session_state["current_page"] = "Settings"
                    st.rerun()
            else:
                st.error(f"❌ Generation Error: {result.get('error')}")

    # Display Result Card if available in session state
    if "last_result" in st.session_state and st.session_state["last_result"]:
        res = st.session_state["last_result"]
        inputs = st.session_state.get("last_inputs", {})

        st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h3 style="font-size: 1.5rem; font-weight: 700; color: #f8fafc;">
                Generated Message Result
            </h3>
        </div>
        """, unsafe_allow_html=True)

        if res.get("warning"):
            st.info(f"ℹ️ {res['warning']}")

        def handle_regeneration():
            """Perform genuine variation regeneration preserving inputs."""
            regen_count = inputs.get("regen_count", 0) + 1
            inputs["regen_count"] = regen_count

            angles = [
                "Use a more direct and punchy opening hook.",
                "Frame the user's achievements with stronger value-add and initiative.",
                "Adopt an even sharper, magnetic communication style while keeping the exact facts.",
                "Structure the sentences differently for maximum readability and conversion."
            ]
            chosen_hint = angles[regen_count % len(angles)]

            with st.spinner("🔄 Crafting fresh perspective with Gemini AI..."):
                new_result = generate_message(
                    platform=inputs["platform"],
                    message_type=inputs["message_type"],
                    recipient=inputs["recipient"],
                    recipient_name=inputs.get("recipient_name"),
                    tone=inputs["tone"],
                    key_points=inputs["key_points"],
                    additional_context=inputs.get("additional_context"),
                    regeneration_prompt_hint=f"Generate a distinctly fresh version. {chosen_hint}"
                )

            if new_result.get("success"):
                st.session_state["last_result"] = new_result
                st.session_state["last_inputs"] = inputs
                # Save fresh version to history
                save_message(
                    platform=inputs["platform"],
                    message_type=inputs["message_type"],
                    recipient=inputs["recipient"],
                    recipient_name=inputs.get("recipient_name"),
                    tone=inputs["tone"],
                    content=new_result["content"],
                    subject=new_result.get("subject"),
                    key_points=inputs["key_points"],
                    additional_context=inputs.get("additional_context")
                )
                st.toast("✨ Fresh version regenerated and saved to history!", icon="🔄")
                st.rerun()
            else:
                st.error(f"❌ Regeneration failed: {new_result.get('error')}")

        render_message_result_card(
            platform=res.get("platform", "Email"),
            content=res.get("content", ""),
            subject=res.get("subject"),
            char_count=res.get("char_count", len(res.get("content", ""))),
            metadata=inputs,
            on_regenerate_callback=handle_regeneration
        )
