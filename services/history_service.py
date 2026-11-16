"""
Database and storage service for BlackHole AI Message History.
Uses SQLite for robust, persistent local storage.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

# Ensure database directory exists
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "history.db")


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS message_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                platform TEXT NOT NULL,
                message_type TEXT NOT NULL,
                recipient TEXT NOT NULL,
                recipient_name TEXT,
                tone TEXT NOT NULL,
                subject TEXT,
                content TEXT NOT NULL,
                char_count INTEGER NOT NULL,
                key_points TEXT,
                additional_context TEXT
            )
        """)
        conn.commit()


def save_message(
    platform: str,
    message_type: str,
    recipient: str,
    recipient_name: Optional[str],
    tone: str,
    content: str,
    subject: Optional[str] = None,
    key_points: Optional[str] = None,
    additional_context: Optional[str] = None
) -> int:
    """Save a generated message to the SQLite database."""
    init_db()
    char_count = len(content)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO message_history (
                platform, message_type, recipient, recipient_name,
                tone, subject, content, char_count, key_points, additional_context
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            platform, message_type, recipient, recipient_name or "",
            tone, subject or "", content, char_count,
            key_points or "", additional_context or ""
        ))
        conn.commit()
        return cursor.lastrowid


def get_all_messages(limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve saved messages sorted by creation date descending."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, created_at, platform, message_type, recipient,
                   recipient_name, tone, subject, content, char_count,
                   key_points, additional_context
            FROM message_history
            ORDER BY datetime(created_at) DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_message_by_id(message_id: int) -> Optional[Dict[str, Any]]:
    """Fetch a single message by ID."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, created_at, platform, message_type, recipient,
                   recipient_name, tone, subject, content, char_count,
                   key_points, additional_context
            FROM message_history
            WHERE id = ?
        """, (message_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def delete_message(message_id: int) -> bool:
    """Delete a specific message by ID."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM message_history WHERE id = ?", (message_id,))
        conn.commit()
        return cursor.rowcount > 0


def clear_all_history() -> bool:
    """Clear all records from message history."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM message_history")
        conn.commit()
        return True


def get_history_stats() -> Dict[str, Any]:
    """Retrieve statistical summary for dashboard."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM message_history")
        total_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM message_history WHERE platform = 'Email'")
        email_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM message_history WHERE platform = 'LinkedIn'")
        linkedin_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT platform, message_type, created_at
            FROM message_history
            ORDER BY datetime(created_at) DESC
            LIMIT 5
        """)
        recent_rows = [dict(r) for r in cursor.fetchall()]

        return {
            "total_messages": total_count,
            "email_messages": email_count,
            "linkedin_messages": linkedin_count,
            "recent_activity": recent_rows
        }
