CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #eef2ff;
    --page: #f5f7ff;
    --panel: rgba(255,255,255,0.95);
    --panel-strong: #ffffff;
    --sidebar: #0c1220;
    --sidebar-2: #101b2b;
    --primary: #2f5ef7;
    --primary-2: #4f46e5;
    --primary-soft: #eaf0ff;
    --secondary: #7c3aed;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --text: #0f172a;
    --muted: #46556f;
    --light-text: #e5ecff;
    --line: #e5e7eb;
    --shadow: 0 18px 38px rgba(15, 23, 42, 0.10);
    --soft-shadow: 0 12px 24px rgba(15, 23, 42, 0.06);
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #eef2ff 0%, #f5f7ff 100%);
    font-family: "Inter", sans-serif;
    color: var(--text);
}

.main {
    background: transparent;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
    max-width: 1500px;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--sidebar) 0%, var(--sidebar-2) 100%);
    color: var(--light-text);
}

[data-testid="stSidebar"] a {
    color: var(--light-text) !important;
    border-radius: 12px;
}

[data-testid="stSidebar"] a[data-selected="true"] {
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-2) 100%);
    color: white !important;
    font-weight: 700;
    border-radius: 12px;
}

[data-testid="stSidebar"] section[data-testid="stSidebarNav"] {
    padding-top: 0.8rem;
}

div[data-testid="stForm"] {
    background: transparent;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select,
.stDateInput input {
    border: 1px solid #d4d9e4 !important;
    border-radius: 12px !important;
    background: white !important;
    color: var(--text) !important;
    padding: 0.7rem 0.85rem !important;
    font-size: 0.96rem !important;
}

.stTextInput label, .stTextArea label, .stDateInput label, .stSelectbox label {
    color: var(--text) !important;
    font-weight: 700 !important;
    margin-bottom: 6px !important;
}

.stButton > button {
    color: white !important;
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-2) 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.72rem 1.3rem !important;
    font-weight: 700 !important;
    box-shadow: 0 12px 20px rgba(79,70,229,0.18);
}

.stButton > button:hover {
    filter: brightness(1.04);
}

.top-banner {
    background: linear-gradient(90deg, #2a52e3 0%, #4f46e5 100%);
    border-radius: 20px;
    padding: 26px 28px;
    margin-bottom: 24px;
    box-shadow: 0 18px 30px rgba(79,70,229,0.18);
    color: white;
}

.top-banner h1 {
    margin: 0;
    color: white !important;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.05em;
}

.top-banner p {
    margin: 8px 0 0 0;
    color: rgba(255,255,255,0.92) !important;
    font-size: 0.96rem;
}

.metric-card {
    background: rgba(255,255,255,0.95);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px 18px 14px 18px;
    box-shadow: var(--soft-shadow);
    min-height: 146px;
    color: var(--text);
}

.metric-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    font-weight: 700;
}

.metric-value {
    font-size: 2.05rem;
    font-weight: 800;
    margin-top: 12px;
    color: var(--text);
    letter-spacing: -0.05em;
}

.section-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 10px;
    letter-spacing: -0.03em;
}

.alert-success {
    color: #047857;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.18);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    font-weight: 700;
    margin: 10px 0;
}

.alert-error {
    color: #b91c1c;
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.18);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    font-weight: 700;
    margin: 10px 0;
}

.card-panel {
    background: rgba(255,255,255,0.96);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px;
    box-shadow: var(--soft-shadow);
    color: var(--text);
}

.dataframe-container {
    overflow: hidden;
    border-radius: 16px;
    border: 1px solid var(--line);
}

.stDataFrame {
    color: var(--text) !important;
    background: white;
}

.stDataFrame td, .stDataFrame th {
    color: var(--text) !important;
    border-color: var(--line) !important;
}

.stTabs [role="tablist"] {
    gap: 12px;
}

.stTabs [role="tab"] {
    background: #edf2ff;
    border-radius: 12px 12px 0 0;
    color: var(--text);
    font-weight: 700;
}

.stTabs [role="tab"][aria-selected="true"] {
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-2) 100%);
    color: white !important;
}

</style>
"""
