"""
'Gate pass' design system.

Token summary (kept here as comments since Streamlit CSS has no var() scoping
across st.markdown calls -- these are the source of truth if colors need to
change later):

  Background   #14161c  (flat ink, no gradient)
  Surface      #1b1e26  (cards, inputs)
  Surface-2    #1e2129  (nav items, subtle raise)
  Border       #2a2d36
  Border (tear)#333844  dashed, used only for the sidebar/content divider
  Text primary #f4f1ea
  Text muted   #8f8f88
  Accent       #e8a33d  (amber -- real trained ML / real LLM calls, primary actions)
  Accent text  #412402  (dark text on amber fills, for contrast)
  Muted accent #2b6f6b  (teal -- rule-based / deterministic features, secondary signal)

  Display font  'Oswald' (headings -- condensed, ticket/signage feel)
  Body font     'Inter'
  Mono font     'JetBrains Mono' (badge numbers, KPI values, data readouts)

Why this direction: event tickets/boarding passes are the one visual object
everyone touching this app already recognizes -- numbered gate stops, a torn
perforation, monospace flight-board numerals. It's specific to the subject
instead of a generic dark dashboard with a purple gradient.
"""

CUSTOM_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">

<style>

:root {
    --bg: #14161c;
    --surface: #1b1e26;
    --surface-2: #1e2129;
    --border: #2a2d36;
    --border-tear: #333844;
    --text-primary: #f4f1ea;
    --text-muted: #8f8f88;
    --accent: #e8a33d;
    --accent-text: #412402;
    --accent-muted: #2b6f6b;
    --accent-muted-text: #d8f3ef;
    --font-display: 'Oswald', sans-serif;
    --font-body: 'Inter', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.001ms !important;
        transition-duration: 0.001ms !important;
    }
}

/* =========================
APP BACKGROUND
========================= */

.stApp {
    background: var(--bg);
    color: var(--text-primary);
    font-family: var(--font-body);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* =========================
TYPOGRAPHY
========================= */

h1 {
    font-family: var(--font-display);
    text-align: left;
    font-size: 2.6rem !important;
    font-weight: 600 !important;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
    letter-spacing: 0.2px;
}

h2, h3 {
    font-family: var(--font-display);
    font-weight: 500 !important;
    color: var(--text-primary);
}

p, label, .stMarkdown {
    color: var(--text-primary);
}

/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px dashed var(--border-tear);
    min-width: 270px !important;
    max-width: 270px !important;
    padding-top: 8px;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 28px;
    margin-top: 12px;
}

.brand-icon {
    width: 38px;
    height: 38px;
    border-radius: 6px;
    border: 1.5px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 700;
    color: var(--accent);
    background: transparent;
}

.brand-title {
    font-family: var(--font-display);
    font-size: 19px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: 0.5px;
}

.brand-subtitle {
    font-size: 12px;
    color: var(--text-muted);
}

.nav-label {
    font-family: var(--font-mono);
    color: var(--text-muted);
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

/* Nav buttons: gate-pass style with a monospace stop number */

section[data-testid="stSidebar"] .stButton {
    width: 100%;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 46px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 0 14px !important;
    margin-bottom: 6px;
    background: var(--surface-2);
    color: var(--text-primary);
    border: 1px solid var(--border);
    border-radius: 6px;
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 500;
    text-align: left;
    transition: background 0.15s ease, border-color 0.15s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #23262f;
    border-color: var(--accent);
    color: var(--text-primary);
}

section[data-testid="stSidebar"] .stButton > button:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}

section[data-testid="stSidebar"] .stButton > button:active {
    transform: scale(0.99);
}

/* =========================
MAIN BUTTONS
========================= */

.stButton>button {
    background: var(--accent);
    color: var(--accent-text);
    border: none;
    border-radius: 6px;
    padding: 0.7rem 1.1rem;
    font-family: var(--font-body);
    font-weight: 600;
    font-size: 15px;
    transition: filter 0.15s ease;
}

.stButton>button:hover {
    filter: brightness(1.08);
}

.stButton>button:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}

.stButton>button:active {
    filter: brightness(0.95);
}

/* =========================
INPUTS
========================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: var(--surface) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
    border: 1px solid var(--border) !important;
    font-family: var(--font-body) !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
}

/* =========================
METRICS
========================= */

div[data-testid="stMetric"] {
    background: var(--surface);
    padding: 18px;
    border-radius: 8px;
    border: 1px solid var(--border);
}

div[data-testid="stMetricValue"] {
    font-family: var(--font-mono) !important;
    color: var(--text-primary) !important;
}

/* =========================
ALERTS -- overridden to match the ink/amber palette instead of
Streamlit's default blue/green/orange tint set
========================= */

div[data-testid="stAlert"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-left: 3px solid var(--accent) !important;
    border-radius: 6px !important;
    color: var(--text-primary) !important;
}

.streamlit-expanderHeader {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text-primary);
}

/* =========================
PAGE FADE (respects reduced motion via the media query above)
========================= */

.block-container {
    animation: fadeIn 0.4s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

/* =========================
GATE-PASS KPI CARDS (Home)
========================= */

.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px;
    text-align: left;
}

.kpi-title {
    font-family: var(--font-mono);
    color: var(--text-muted);
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 1px;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.kpi-value {
    font-family: var(--font-mono);
    color: var(--accent);
    font-size: 26px;
    font-weight: 700;
}

/* =========================
FEATURE CARDS (Home) -- accent = real trained ML/LLM, muted = rule-based/NLP
========================= */

.feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--border);
    border-radius: 8px;
    padding: 18px 20px;
    margin-bottom: 12px;
}

.feature-card.is-real-ai {
    border-left-color: var(--accent);
}

.feature-card.is-rule-based {
    border-left-color: var(--accent-muted);
}

.feature-card-title {
    font-family: var(--font-display);
    font-size: 17px;
    font-weight: 500;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.feature-card-tag {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
    vertical-align: middle;
}

.feature-card.is-real-ai .feature-card-tag {
    background: rgba(232, 163, 61, 0.15);
    color: var(--accent);
}

.feature-card.is-rule-based .feature-card-tag {
    background: rgba(43, 111, 107, 0.2);
    color: #6fd1c9;
}

.feature-card-desc {
    font-size: 13px;
    color: var(--text-muted);
    margin: 0;
}

/* =========================
FOOTER
========================= */

.custom-footer {
    margin-top: 50px;
    padding: 16px 0;
    text-align: left;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 12px;
    border-top: 1px dashed var(--border-tear);
}
</style>
"""
