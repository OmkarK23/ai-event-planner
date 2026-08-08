"""Custom dark-theme CSS for the app. Extracted from the original single-file
main.py so styling can be reviewed/edited independently of page logic."""

CUSTOM_CSS = """
<style>

/* =========================
APP BACKGROUND
========================= */

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 45%,
        #1e1b4b 100%
    );
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* =========================
TYPOGRAPHY
========================= */

h1 {
    text-align: center;
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: white;
    margin-bottom: 0.5rem;
}

h2, h3 {
    color: #e0e7ff;
}

/* =========================
PREMIUM SIDEBAR NAV
========================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #020617 0%,
        #071126 100%
    );
    border-right: 1px solid #1e293b;
    min-width: 280px !important;
    max-width: 280px !important;
    padding-top: 10px;
}

section[data-testid="stSidebar"] .stButton {
    width: 100%;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    height: 78px !important;
    min-height: 78px !important;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 0 22px !important;
    margin-bottom: 16px;
    background: rgba(15,23,42,0.85);
    color: #e2e8f0;
    border: 1px solid rgba(100, 116, 139, 0.35);
    border-radius: 22px;
    font-size: 15px;
    font-weight: 650;
    line-height: 1.25;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.22);
    transition: all .35s ease;
    text-align: left;
    overflow: hidden;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(90deg, #2563eb, #7c3aed, #ec4899);
    color: white;
    transform: translateX(8px) scale(1.03);
    border: 1px solid #818cf8;
    box-shadow: 0 18px 36px rgba(124, 58, 237, 0.42);
}

section[data-testid="stSidebar"] .stButton > button:active {
    transform: scale(.98);
}

/* Sidebar brand */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 35px;
    margin-top: 15px;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: white;
    box-shadow: 0 10px 25px rgba(168, 85, 247, 0.4);
}

.brand-title {
    font-size: 22px;
    font-weight: 800;
    color: white;
}

.brand-subtitle {
    font-size: 13px;
    color: #94a3b8;
}

.nav-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
}

/* =========================
MAIN BUTTONS
========================= */

.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    font-weight: 700;
    font-size: 16px;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(236, 72, 153, 0.35);
}

/* =========================
INPUTS
========================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #475569 !important;
}

/* =========================
METRICS
========================= */

div[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.85);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #475569;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
}

/* =========================
FEATURE CARDS
========================= */

.feature-card {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(12px);
    transition: all 0.35s ease;
}

.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.35);
    border: 1px solid rgba(99, 102, 241, 0.45);
}

/* =========================
ALERTS + EXPANDERS
========================= */

.streamlit-expanderHeader {
    background-color: #1e293b;
    border-radius: 10px;
}

.stAlert {
    border-radius: 14px;
}

/* =========================
PAGE FADE ANIMATION
========================= */

.block-container {
    animation: fadeIn 0.55s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

/* =========================
GLASS KPI CARDS
========================= */

.kpi-card {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-6px);
    border: 1px solid rgba(129, 140, 248, 0.7);
    box-shadow: 0 18px 38px rgba(124,58,237,0.35);
}

.kpi-title {
    color: #94a3b8;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 8px;
}

.kpi-value {
    color: white;
    font-size: 30px;
    font-weight: 900;
}

/* =========================
FOOTER BRANDING
========================= */

.custom-footer {
    margin-top: 60px;
    padding: 20px;
    text-align: center;
    color: #94a3b8;
    font-size: 14px;
    border-top: 1px solid rgba(148,163,184,0.2);
}
</style>
"""
