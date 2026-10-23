* {
  box-sizing: border-box;
}

:root {
  --bg: #f3f7fb;
  --surface: #ffffff;
  --surface-soft: #eef4ff;
  --primary: #1d4ed8;
  --primary-strong: #163ea8;
  --text: #10213a;
  --muted: #5a6b81;
  --success: #157f5b;
  --success-soft: #dff7ee;
  --warning: #b96c00;
  --warning-soft: #fff0d9;
  --border: #dfe7f1;
}

body {
  margin: 0;
  font-family: Inter, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
}

button {
  border: none;
  cursor: pointer;
}

.app-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px 56px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
}

.topbar h1 {
  margin: 8px 0 0;
  font-size: 2rem;
}

.primary-btn {
  background: var(--primary);
  color: white;
  padding: 12px 18px;
  border-radius: 10px;
  font-weight: 600;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 18px;
  margin-bottom: 24px;
}

.kpi-card,
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(16, 33, 58, 0.04);
}

.kpi-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.kpi-card span {
  color: var(--muted);
  font-size: 0.9rem;
}

.kpi-card strong {
  font-size: 2rem;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
  margin-bottom: 24px;
}

.panel {
  padding: 20px;
}

.panel h2 {
  margin-top: 0;
  font-size: 1.2rem;
}

.alert-list {
  margin: 0;
  padding-left: 18px;
  color: var(--text);
  line-height: 1.8;
}

.bars {
  display: flex;
  align-items: end;
  gap: 18px;
  height: 180px;
  padding-top: 18px;
}

.bar-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.bar-stack {
  display: flex;
  align-items: end;
  gap: 6px;
  height: 140px;
}

.bar {
  display: block;
  width: 18px;
  border-radius: 10px 10px 0 0;
}

.bar.attendance {
  background: var(--primary);
}

.bar.fees {
  background: #7da6ff;
}

.bar-group label {
  color: var(--muted);
  font-size: 0.8rem;
}

.table-panel {
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th,
td {
  padding: 14px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

th {
  color: var(--muted);
  background: var(--surface-soft);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.status {
  display: inline-flex;
  align-items: center;
  padding: 7px 10px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status.good {
  background: var(--success-soft);
  color: var(--success);
}

.status.warn {
  background: var(--warning-soft);
  color: var(--warning);
}

.loading {
  min-height: 100vh;
  display: grid;
  place-items: center;
  font-size: 1.2rem;
  color: var(--muted);
}

@media (max-width: 640px) {
  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }

  .app-shell {
    padding-left: 14px;
    padding-right: 14px;
  }
}
