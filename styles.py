CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --page-bg: #f3f6ff;
    --panel: rgba(255,255,255,0.96);
    --panel-soft: #f7f9ff;
    --primary: #2f5ef7;
    --primary-2: #4f46e5;
    --primary-soft: #e9f0ff;
    --success: #17b26a;
    --warning: #f59e0b;
    --danger: #ef4444;
    --text: #101828;
    --muted: #5d6b82;
    --line: #e5e7eb;
    --sidebar: #0b1220;
    --sidebar-2: #101b2a;
    --nav-text: #eaf1ff;
    --shadow: 0 18px 38px rgba(18, 24, 38, 0.09);
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #edf2ff 0%, #f7f9ff 100%);
    font-family: "Inter", sans-serif;
    color: var(--text);
}

.main {
    background: transparent;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1550px;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--sidebar) 0%, var(--sidebar-2) 100%);
    color: var(--nav-text);
}

[data-testid="stSidebar"] a {
    color: var(--nav-text) !important;
    border-radius: 12px;
}

[data-testid="stSidebar"] a[data-selected="true"] {
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-2) 100%);
    color: white !important;
    font-weight: 700;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select,
.stDateInput input {
    border: 1px solid #d5dae5 !important;
    border-radius: 12px !important;
    padding: 0.7rem 0.9rem !important;
    color: var(--text) !important;
    background: white !important;
}

.stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {
    color: var(--text) !important;
    font-weight: 700 !important;
}

.stButton > button {
    border: none !important;
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-2) 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.35rem !important;
    font-weight: 700 !important;
    box-shadow: 0 12px 20px rgba(79,70,229,0.18);
}

.top-banner {
    background: linear-gradient(90deg, #2c53e5 0%, #4f46e5 100%);
    padding: 26px 28px;
    border-radius: 20px;
    box-shadow: 0 18px 30px rgba(79,70,229,0.17);
    margin-bottom: 22px;
    color: white;
}

.top-banner h1 {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    color: white !important;
}

.top-banner p {
    margin: 10px 0 0 0;
    font-size: 0.96rem;
    color: rgba(255,255,255,0.92) !important;
}

.metric-card {
    background: rgba(255,255,255,0.97);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px 18px 14px 18px;
    min-height: 146px;
    box-shadow: 0 12px 24px rgba(15, 23, 42, 0.05);
}

.metric-label {
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--muted);
}

.metric-value {
    font-size: 2.1rem;
    font-weight: 800;
    margin-top: 12px;
    color: var(--text);
    letter-spacing: -0.05em;
}

.panel {
    background: rgba(255,255,255,0.97);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 12px 24px rgba(15, 23, 42, 0.05);
}

.section-title {
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text);
    margin-bottom: 10px;
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

.stDataFrame td, .stDataFrame th {
    color: var(--text) !important;
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

.status-badge {
    display: inline-block;
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.status-paid {
    background: rgba(16,185,129,0.12);
    color: #047857;
}

.status-pending {
    background: rgba(245,158,11,0.12);
    color: #b45309;
}

.status-overdue {
    background: rgba(239,68,68,0.12);
    color: #b91c1c;
}

</style>
"""
