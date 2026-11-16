"""
Reusable UI Components and Visual Elements for BlackHole AI.
"""

import streamlit as st
import html
import json


def render_logo(size: int = 40):
    """Render the BlackHole AI futuristic glowing logo."""
    return f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">
        <div style="
            width: {size}px; 
            height: {size}px; 
            border-radius: 50%; 
            background: radial-gradient(circle at 35% 35%, #050508 20%, #3b0764 65%, #a855f7 90%, #38bdf8 100%);
            box-shadow: 0 0 18px 2px rgba(168, 85, 247, 0.6), inset 0 0 10px #000;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        ">
            <div style="width: {size//3}px; height: {size//3}px; background: #000; border-radius: 50%;"></div>
        </div>
        <div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 700; letter-spacing: -0.03em; line-height: 1.1;">
                <span style="color: #ffffff;">BlackHole</span> <span style="background: linear-gradient(135deg, #c084fc, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI</span>
            </div>
            <div style="font-size: 0.68rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600;">Message Architect</div>
        </div>
    </div>
    """


def render_hero_badge(text: str = "Gravitational Career Intelligence"):
    """Render cosmic badge."""
    return f"""
    <div style="margin-bottom: 0.75rem;">
        <span class="bh-badge">
            <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#c084fc; box-shadow:0 0 8px #c084fc;"></span>
            {text}
        </span>
    </div>
    """


def render_black_hole_visual():
    """Render interactive-feel gravitational event horizon visual element."""
    return """
    <div style="text-align: center; margin: 1.5rem 0 2rem 0;">
        <div class="bh-horizon-circle">
            <div style="position: absolute; inset: 12px; border-radius: 50%; border: 1px dashed rgba(168, 85, 247, 0.4); animation: spin 20s linear infinite;"></div>
            <div style="position: absolute; inset: 25px; border-radius: 50%; border: 1px dotted rgba(56, 189, 248, 0.5); animation: spin-reverse 15s linear infinite;"></div>
            <div style="position: absolute; inset: 38px; border-radius: 50%; background: #020204; box-shadow: inset 0 0 15px rgba(0,0,0,0.9);"></div>
        </div>
        <style>
            @keyframes spin { 100% { transform: rotate(360deg); } }
            @keyframes spin-reverse { 100% { transform: rotate(-360deg); } }
        </style>
    </div>
    """


def render_feature_card(title: str, description: str, tag: str = "AI Powered", icon: str = "⚡"):
    """Render an individual feature showcase card."""
    return f"""
    <div class="bh-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <span class="bh-badge bh-badge-cyan" style="font-size: 0.7rem;">{tag}</span>
            </div>
            <h3 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem; color: #f8fafc;">{title}</h3>
            <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin-bottom: 1rem;">{description}</p>
        </div>
        <div style="font-size: 0.75rem; color: #a855f7; font-weight: 600; display: flex; align-items: center; gap: 4px;">
            Optimized for Conversions &rarr;
        </div>
    </div>
    """


def render_copy_script():
    """Inject robust browser-safe clipboard copying helper."""
    return """
    <script>
    function copyToClipboard(text, elementId) {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(function() {
                var el = document.getElementById(elementId);
                if (el) {
                    var oldText = el.innerText;
                    el.innerText = 'Copied!';
                    setTimeout(function() { el.innerText = oldText; }, 2000);
                }
            }).catch(function(err) {
                fallbackCopy(text);
            });
        } else {
            fallbackCopy(text);
        }
    }
    function fallbackCopy(text) {
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.top = "-9999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            alert('Copied to clipboard!');
        } catch (err) {
            prompt("Copy manually:", text);
        }
        document.body.removeChild(textArea);
    }
    </script>
    """
