# 🌌 BlackHole AI – Professional Message Writer

[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

**BlackHole AI** is a production-quality, premium web application built for students, recent graduates, and career transitioners to craft compelling, high-converting professional communications—from magnetic cold emails to strictly enforced 300-character LinkedIn connection notes—powered by Google Gemini AI.

---

## 🚀 Key Features

- **Deep Space Visual Identity:** Glassmorphic UI with event horizon animations, electric purple accents, cosmic particle glows, and typography.
- **✉️ Professional Email Generator:** High-open-rate subject lines, personalized greetings, tailored pitches weaving in verified user points, and clear calls-to-action (CTA).
- **🔗 LinkedIn Message Generator:** **Strictly enforces &le; 300 characters** with a live visual counter, built specifically for LinkedIn connection requests and InMails.
- **🔄 Intelligent Variation Regeneration:** Generates distinct perspectives without robotic repetition or losing factual points.
- **📁 Persistent SQLite History:** Local storage of past drafts. Copy, reopen in generator, or delete records.
- **🛡️ Enterprise Privacy & Zero Hallucination:** Strict prompt engineering ensures the AI never hallucinates unmentioned metrics or degrees. API keys are strictly kept server-side.
- **📱 Responsive & Interactive:** Full mobile/desktop responsive design with built-in clipboard copying.

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit 1.35+
- **Backend & Logic:** Python 3.10+ / Python 3.14
- **AI Engine:** Google Gemini (`gemini-3.5-flash`) via the official `google-genai` SDK
- **Styling:** Custom CSS with Glassmorphism, animations, and Space Grotesk / Plus Jakarta Sans fonts
- **Database:** Local SQLite (`database/history.db`)
- **Environment Management:** `python-dotenv` & Streamlit Secrets

---

## 📦 Project Structure

```
Writer/
│
├── app.py                     # Main orchestrator & page routing
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Version control ignores
├── README.md                  # Complete documentation
│
├── pages/                     # Application pages
│   ├── home.py                # Dashboard & hero landing
│   ├── generator.py           # Core message generation engine
│   ├── history.py             # Persistent message archive
│   ├── settings.py            # Gemini API status & preferences
│   └── about.py               # Tech stack & architecture details
│
├── components/                # Reusable UI modules
│   ├── sidebar.py             # Navigation hub & system status
│   ├── message_card.py        # Result card with copy & regen actions
│   └── ui_components.py       # Logos, badges, and black-hole animations
│
├── services/                  # Business & backend services
│   ├── gemini_service.py      # Google GenAI SDK integration & limit verification
│   └── history_service.py     # SQLite persistence engine & stats
│
├── database/                  # Storage directory
│   └── history.db             # Auto-created SQLite database
│
├── assets/                    # Styling & static assets
│   └── background.css         # Black hole deep space stylesheet
│
└── .streamlit/
    └── secrets.toml.example   # Streamlit secrets template
```

---

## ⚡ Windows Quickstart & Installation

Follow these steps to set up and run BlackHole AI on Windows:

### 1. Clone or Open Workspace
Open PowerShell in the project directory:
```powershell
cd "c:\Users\VISHNU NARAYANAN K\Downloads\Writer"
```

### 2. Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

### 3. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key
Get a free API key from [Google AI Studio](https://aistudio.google.com/).

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
*(Alternatively, configure it inside the running app via the **Settings** page or `.streamlit/secrets.toml`)*

### 5. Launch Application
```powershell
streamlit run app.py
```
The application will launch automatically in your browser at `http://localhost:8501`.

---

## 🧪 Testing Checklist

- [x] Application launches cleanly via `streamlit run app.py`
- [x] All 5 pages navigate reliably from the sidebar and internal action buttons
- [x] Gemini AI integration securely calls `gemini-3.5-flash`
- [x] LinkedIn generator strictly enforces and validates $\le 300$ character ceiling
- [x] Email generator produces clean Subject and Body fields
- [x] Regeneration button creates a novel version without losing parameters
- [x] Message history persists across reboots in `database/history.db`
- [x] Copy buttons provide instant clipboard code blocks and toast notifications
- [x] History delete and clear-all operations work with verification

---

## 🔧 Troubleshooting

| Issue | Resolution |
|---|---|
| **API Key Missing Warning** | Add `GEMINI_API_KEY=your_key` in `.env` or input it directly in **Settings > Runtime Session API Key Override**. |
| **Execution Policy Error in PowerShell** | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before activating the virtual environment. |
| **LinkedIn Message Length** | BlackHole AI automatically validates the output against the 300-character limit and trims if necessary. |
| **Port Conflict (8501)** | Run `streamlit run app.py --server.port 8502`. |

---

## 📄 License
MIT License. Built for students, engineers, and creators worldwide.
