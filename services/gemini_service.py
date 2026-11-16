"""
Gemini AI Service integration for BlackHole AI.
Powered by the official Google GenAI SDK (google-genai).
"""

import os
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()


def get_api_key() -> Optional[str]:
    """
    Retrieve Gemini API key from environment variables or Streamlit secrets.
    Does not expose secrets.
    """
    # 1. Check OS environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and api_key.strip():
        return api_key.strip()

    # 2. Check Streamlit secrets if running inside streamlit
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"].strip()
    except Exception:
        pass

    return None


def is_api_key_configured() -> bool:
    """Return True if an API key is present."""
    key = get_api_key()
    return bool(key and len(key) > 5)


def clean_markdown_blocks(text: str) -> str:
    """Strip extraneous outer markdown code fences if Gemini returns them."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned.strip()


def parse_email_response(raw_text: str) -> Dict[str, str]:
    """Extract Subject and Body cleanly from model output."""
    raw_text = clean_markdown_blocks(raw_text)
    subject = "Professional Communication"
    body = raw_text

    # Match "Subject: ..." at the start or on a line
    match = re.search(r"^(?:Subject|SUBJECT):\s*(.+)$", raw_text, re.MULTILINE)
    if match:
        subject = match.group(1).strip()
        # Remove the subject line and any immediate blank lines from body
        body = re.sub(r"^(?:Subject|SUBJECT):\s*.+$\n*", "", raw_text, flags=re.MULTILINE).strip()

    return {
        "subject": subject,
        "body": body
    }


def generate_message(
    platform: str,
    message_type: str,
    recipient: str,
    recipient_name: Optional[str],
    tone: str,
    key_points: str,
    additional_context: Optional[str] = None,
    regeneration_prompt_hint: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate professional message using Gemini API.
    Handles strict LinkedIn character limits and Email structuring.
    """
    api_key = get_api_key()
    if not api_key:
        return {
            "success": False,
            "error_type": "MISSING_KEY",
            "error": "Gemini API key is not configured. Please add GEMINI_API_KEY to your environment variables or .streamlit/secrets.toml."
        }

    recipient_display = recipient_name.strip() if recipient_name and recipient_name.strip() else f"the {recipient}"

    # Build the system prompt & instructions based on platform
    system_instruction = (
        "You are BlackHole AI, an elite career communication architect who writes detailed, "
        "comprehensive, and polished professional messages. You are expert at crafting full-length "
        "professional emails and LinkedIn messages for students, fresh graduates, and job seekers.\n\n"
        "CRITICAL RULES:\n"
        "1. NEVER fabricate experiences, metrics, qualifications, or degrees not explicitly mentioned by the user.\n"
        "2. Avoid generic corporate fluff, excessive flattery, and robotic filler phrases.\n"
        "3. Ensure the tone is genuinely human, confident, and respectful.\n"
        "4. Follow platform constraints religiously.\n"
        "5. For EMAILS: Always write COMPLETE, DETAILED emails with multiple well-developed paragraphs. "
        "NEVER write a short 1-2 sentence email. Minimum 150 words for the email body.\n"
        "6. Use natural, flowing language that sounds like a real person wrote it."
    )

    if platform == "LinkedIn":
        user_prompt = f"""Write a high-converting LinkedIn connection note or InMail for {recipient_display} ({recipient}).

Context:
- Message Category: {message_type}
- Platform: LinkedIn (STRICT CHARACTER LIMIT: MAXIMUM 300 CHARACTERS INCLUDING SPACES)
- Desired Tone: {tone}
- Key Points to Include: {key_points}
- Additional Context: {additional_context or 'None provided'}

CRITICAL REQUIREMENTS:
- The ENTIRE message MUST be under 300 characters total (including spaces).
- Skip generic greetings like "I hope this finds you well."
- Be concise, direct, engaging, and action-oriented.
- Make every word count within the 300 character limit.
{f"- Variation instruction: {regeneration_prompt_hint}" if regeneration_prompt_hint else ""}

Output ONLY the raw LinkedIn message text. No quotes, no markdown, no headers, no explanations.
"""
    else:  # Email
        user_prompt = f"""Write a COMPLETE, DETAILED, and PROFESSIONAL email to {recipient_display} ({recipient}).

Context:
- Message Category: {message_type}
- Platform: Professional Email
- Desired Tone: {tone}
- Key Points to Include: {key_points}
- Additional Context: {additional_context or 'None provided'}

IMPORTANT - EMAIL STRUCTURE REQUIREMENTS:
You MUST write a FULL-LENGTH professional email with ALL of these sections:

1. SUBJECT LINE: Start the very first line with "Subject: " followed by a compelling, specific subject line.

2. GREETING: Write an appropriate greeting addressing {recipient_display if recipient_name else '[Recipient Name]'}.

3. OPENING PARAGRAPH (2-3 sentences): State the purpose of the email clearly. Mention how you found the opportunity or why you are reaching out.

4. BODY PARAGRAPH 1 (3-4 sentences): Elaborate on your key qualifications, skills, and experiences mentioned in the key points. Connect them to the role or opportunity.

5. BODY PARAGRAPH 2 (2-3 sentences): Express genuine enthusiasm for the specific company/role/opportunity. Mention any relevant additional context provided.

6. CLOSING PARAGRAPH (2-3 sentences): Include a clear, polite call-to-action (e.g., requesting a meeting, expressing availability for interview, asking to discuss further). Express gratitude for their time and consideration.

7. SIGN-OFF: Professional closing (e.g., "Best regards," or "Sincerely,") followed by "[Your Full Name]" as a placeholder.

QUALITY REQUIREMENTS:
- The email body MUST be at least 150 words and well-developed.
- DO NOT write a short 1-2 sentence email. Write a COMPLETE professional email.
- Weave ALL the user's key points naturally into the email body.
- Make the email sound human, warm, and genuine — not robotic.
- Use proper paragraph breaks between sections.
{f"- Variation instruction: {regeneration_prompt_hint}" if regeneration_prompt_hint else ""}

Write the complete email now, starting with "Subject: " on the first line.
"""

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        # gemini-3.5-flash is the confirmed free working model for new API keys.
        # Fallback chain retries next only on 404/503 errors.
        models_to_try = [
            "gemini-3.5-flash",       # Primary: confirmed working free tier
            "gemini-3.5-flash-lite",  # Fallback 1
            "gemini-3.1-flash-lite",  # Fallback 2
            "gemini-3.8-flash",       # Fallback 3 (high demand, may timeout)
        ]

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.75 if regeneration_prompt_hint else 0.6,
            max_output_tokens=3500
        )

        response = None
        last_exception = None
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_prompt,
                    config=config
                )
                if response and response.text:
                    break
            except Exception as ex:
                last_exception = ex
                continue

        if not response or not response.text:
            if last_exception:
                raise last_exception
            return {
                "success": False,
                "error_type": "EMPTY_RESPONSE",
                "error": "The AI model returned an empty response. Please try again."
            }

        generated_text = response.text.strip()

        if platform == "LinkedIn":
            cleaned_text = clean_markdown_blocks(generated_text)
            # Enforce strict 300 char verification
            char_len = len(cleaned_text)
            if char_len > 300:
                # Fallback trimming or concise adjustment if model slightly overshot
                trimmed = cleaned_text[:297] + "..."
                return {
                    "success": True,
                    "platform": "LinkedIn",
                    "subject": None,
                    "content": trimmed,
                    "char_count": len(trimmed),
                    "warning": f"AI response was {char_len} characters and was trimmed to meet LinkedIn's 300 character limit."
                }
            return {
                "success": True,
                "platform": "LinkedIn",
                "subject": None,
                "content": cleaned_text,
                "char_count": char_len
            }
        else:
            parsed = parse_email_response(generated_text)
            return {
                "success": True,
                "platform": "Email",
                "subject": parsed["subject"],
                "content": parsed["body"],
                "char_count": len(parsed["body"])
            }

    except Exception as e:
        error_msg = str(e)
        error_type = "API_ERROR"
        if "API_KEY_INVALID" in error_msg or "invalid api key" in error_msg.lower() or "400" in error_msg:
            error_type = "INVALID_KEY"
            user_friendly = "Invalid Gemini API Key. Please verify your API key in Settings or .env file."
        elif "quota" in error_msg.lower() or "429" in error_msg:
            error_type = "QUOTA_EXCEEDED"
            user_friendly = "Gemini API rate limit or quota exceeded. Please wait a moment or check your account."
        elif "404" in error_msg or "NOT_FOUND" in error_msg:
            error_type = "MODEL_UNAVAILABLE"
            user_friendly = (
                "The Gemini model is not available for your API key. "
                "Please verify your API key is valid and active at Google AI Studio."
            )
        elif "503" in error_msg or "UNAVAILABLE" in error_msg:
            error_type = "SERVICE_UNAVAILABLE"
            user_friendly = "Gemini API is temporarily experiencing high demand. Please try again in a few seconds."
        else:
            user_friendly = f"Gemini API error: {error_msg}"

        return {
            "success": False,
            "error_type": error_type,
            "error": user_friendly
        }
