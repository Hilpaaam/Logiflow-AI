from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# In-memory "database" for demo
audit_requests = []

# Template (HTML + CSS in one string)
PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>LogiFlow AI – Agentic Logistics Intelligence</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary-blue: #e3f2ff;
            --primary-blue-strong: #2a6fdd;
            --primary-blue-soft: #b7d6ff;
            --cream: #fff7e6;
            --cream-deep: #f3e0c8;
            --dark-text: #102040;
            --muted-text: #4a5c7a;
            --border-soft: #d5e2ff;
            --accent-green: #26a69a;
            --accent-red: #ff5252;
            --card-radius: 14px;
            --shadow-soft: 0 16px 40px rgba(15, 35, 80, 0.12);
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: linear-gradient(135deg, var(--primary-blue), var(--cream));
            color: var(--dark-text);
        }

        .page-wrap {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            padding: 18px 7%;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            font-size: 1.1rem;
            color: var(--dark-text);
        }

        .logo-mark {
            width: 32px;
            height: 32px;
            border-radius: 12px;
            background: radial-gradient(circle at 20% 20%, #ffffff, var(--primary-blue-soft));
            border: 1px solid rgba(255,255,255,0.9);
            box-shadow: 0 6px 18px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            color: var(--primary-blue-strong);
        }

        nav {
            display: flex;
            gap: 20px;
            font-size: 0.9rem;
        }

        nav a {
            text-decoration: none;
            color: var(--muted-text);
        }

        .cta-header {
            padding: 8px 16px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.9);
            background: rgba(255,255,255,0.85);
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--primary-blue-strong);
        }

        main {
            flex: 1;
            padding: 12px 7% 40px 7%;
        }

        .hero {
            display: grid;
            grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
            gap: 32px;
            align-items: center;
        }

        @media (max-width: 900px) {
            .hero {
                grid-template-columns: 1fr;
            }
            header {
                padding: 14px 5%;
            }
            main {
                padding: 10px 5% 32px 5%;
            }
            nav {
                display: none;
            }
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.9);
            border: 1px solid rgba(181, 203, 255, 0.8);
            font-size: 0.75rem;
            color: var(--muted-text);
            margin-bottom: 10px;
        }

        .badge span {
            padding: 3px 8px;
            border-radius: 999px;
            background: #d1e2ff;
            font-weight: 600;
            color: var(--primary-blue-strong);
        }

        h1 {
            font-size: 2.3rem;
            margin: 0 0 10px 0;
            color: var(--dark-text);
        }

        .hero-subtitle {
            font-size: 1rem;
            color: var(--muted-text);
            margin-bottom: 14px;
        }

        .hero-highlight {
            font-size: 0.95rem;
            color: var(--dark-text);
            background: rgba(255,247,230,0.95);
            border-left: 3px solid var(--cream-deep);
            padding: 10px 12px;
            border-radius: 12px;
            margin-bottom: 18px;
        }

        .hero-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 10px;
            margin-bottom: 18px;
        }

        .hero-pill {
            font-size: 0.85rem;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.96);
            border: 1px solid rgba(213,226,255,0.9);
            color: var(--muted-text);
        }

        .hero-pill strong {
            color: var(--dark-text);
        }

        .hero-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
        }

        .btn-primary {
            background: radial-gradient(circle at 10% 0, #ffffff, var(--primary-blue-strong));
            color: white;
            border-radius: 999px;
            padding: 10px 18px;
            border: none;
            cursor: pointer;
            font-size: 0.95rem;
            font-weight: 600;
            box-shadow: 0 10px 24px rgba(11, 60, 160, 0.30);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary span {
            font-size: 1.1rem;
        }

        .btn-ghost {
            background: rgba(255,255,255,0.9);
            color: var(--muted-text);
            border-radius: 999px;
            padding: 9px 14px;
            border: 1px solid rgba(190, 205, 240, 0.9);
            cursor: pointer;
            font-size: 0.85rem;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .trust-text {
            font-size: 0.75rem;
            color: var(--muted-text);
            margin-top: 6px;
        }

        .hero-right {
            background: rgba(255,255,255,0.96);
            border-radius: 24px;
            padding: 18px 18px 16px 18px;
            box-shadow: var(--shadow-soft);
            border: 1px solid rgba(201, 215, 255, 0.9);
        }

        .panel-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }

        .panel-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--dark-text);
        }

        .panel-chip {
            font-size: 0.75rem;
            padding: 4px 9px;
            border-radius: 999px;
            background: rgba(227,242,255,0.9);
            color: var(--primary-blue-strong);
            border: 1px solid rgba(180,204,255,0.9);
        }

        .mini-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
            margin-bottom: 10px;
        }

        .mini-card {
            background: linear-gradient(145deg, #fefefe, #f3f5ff);
            border-radius: 16px;
            padding: 10px;
            border: 1px solid var(--border-soft);
            font-size: 0.8rem;
        }

        .mini-label {
            font-size: 0.7rem;
            color: var(--muted-text);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 4px;
        }

        .mini-value {
            font-size: 0.9rem;
            color: var(--dark-text);
        }

        .status-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 9px 10px;
            border-radius: 14px;
            background: linear-gradient(90deg, rgba(38,166,154,0.08), rgba(255,247,230,0.7));
            font-size: 0.8rem;
            margin-bottom: 10px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 8px;
            border-radius: 999px;
            background: rgba(255,255,255,0.9);
            border: 1px solid rgba(198,223,255,0.9);
            font-size: 0.75rem;
            color: var(--muted-text);
        }

        .status-pill-dot {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: var(--accent-green);
        }

        .status-metric {
            font-size: 0.8rem;
            color: var(--muted-text);
        }

        .status-metric strong {
            color: var(--dark-text);
        }

        .timeline {
            margin-top: 6px;
            border-radius: 16px;
            padding: 10px;
            background: rgba(247,250,255,0.95);
            border: 1px dashed rgba(188,210,255,0.9);
            font-size: 0.78rem;
        }

        .timeline-row {
            display: flex;
            gap: 10px;
            margin-bottom: 6px;
        }

        .timeline-tag {
            min-width: 60px;
            padding: 3px 6px;
            border-radius: 999px;
            background: rgba(255,247,230,0.9);
            color: #b36b00;
            font-size: 0.75rem;
            text-align: center;
        }

        .timeline-text {
            color: var(--muted-text);
        }

        .section {
            margin-top: 32px;
        }

        .section-title {
            font-size: 1.1rem;
            margin-bottom: 4px;
        }

        .section-subtitle {
            font-size: 0.85rem;
            color: var(--muted-text);
            margin-bottom: 10px;
        }

        .grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 14px;
        }

        .card {
            background: rgba(255,255,255,0.96);
            border-radius: var(--card-radius);
            padding: 12px;
            border: 1px solid rgba(205,215,240,0.95);
            box-shadow: 0 10px 28px rgba(17, 42, 90, 0.08);
            font-size: 0.85rem;
        }

        .card h3 {
            font-size: 0.95rem;
            margin: 0 0 6px 0;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 6px;
        }

        .pill {
            font-size: 0.75rem;
            padding: 4px 8px;
            border-radius: 999px;
            background: rgba(227,242,255,0.9);
            color: var(--muted-text);
        }

        .pill-cream {
            background: rgba(255,247,230,0.9);
            color: #b36b00;
        }

        .compare {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 14px;
            margin-top: 10px;
        }

        .compare-block h4 {
            margin: 0 0 6px 0;
            font-size: 0.9rem;
        }

        .compare-item {
            font-size: 0.8rem;
            display: flex;
            gap: 6px;
            align-items: flex-start;
            margin-bottom: 4px;
        }

        .compare-icon {
            width: 16px;
            height: 16px;
            border-radius: 999px;
            flex-shrink: 0;
            margin-top: 2px;
        }

        .compare-icon.bad {
            background: var(--accent-red);
        }

        .compare-icon.good {
            background: var(--accent-green);
        }

        .objections-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 14px;
            margin-top: 10px;
        }

        .objection-title {
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .objection-q {
            font-size: 0.82rem;
            color: var(--muted-text);
            margin-bottom: 6px;
        }

        .objection-a {
            font-size: 0.8rem;
        }

        .audit-section {
            margin-top: 32px;
            display: grid;
            grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr);
            gap: 22px;
        }

        @media (max-width: 900px) {
            .audit-section {
                grid-template-columns: 1fr;
            }
        }

        .audit-copy {
            font-size: 0.9rem;
        }

        .audit-copy ul {
            padding-left: 16px;
            margin-top: 6px;
        }

        .audit-copy li {
            font-size: 0.85rem;
            margin-bottom: 4px;
        }

        .form-card {
            background: rgba(255,255,255,0.98);
            border-radius: 18px;
            padding: 14px;
            border: 1px solid rgba(203, 213, 240, 0.95);
            box-shadow: 0 10px 26px rgba(17, 24, 39, 0.12);
            font-size: 0.85rem;
        }

        .form-header {
            margin-bottom: 8px;
        }

        .form-header h3 {
            margin: 0 0 4px 0;
            font-size: 0.95rem;
        }

        .form-header p {
            margin: 0;
            font-size: 0.8rem;
            color: var(--muted-text);
        }

        .field-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 8px;
        }

        .field {
            margin-bottom: 8px;
        }

        label {
            display: block;
            font-size: 0.8rem;
            margin-bottom: 2px;
            color: var(--muted-text);
        }

        input, textarea, select {
            width: 100%;
            padding: 7px 8px;
            border-radius: 8px;
            border: 1px solid rgba(198, 211, 245, 0.95);
            font-family: inherit;
            font-size: 0.8rem;
            outline: none;
            background: rgba(248, 250, 255, 0.9);
        }

        textarea {
            min-height: 70px;
            resize: vertical;
        }

        input:focus, textarea:focus {
            border-color: var(--primary-blue-strong);
            box-shadow: 0 0 0 1px rgba(42,111,221,0.12);
            background: #ffffff;
        }

        .form-footer {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 10px;
            margin-top: 6px;
        }

        .form-note {
            font-size: 0.75rem;
            color: var(--muted-text);
        }

        footer {
            padding: 16px 7% 18px 7%;
            font-size: 0.8rem;
            color: var(--muted-text);
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 8px;
        }

        footer a {
            color: var(--muted-text);
            text-decoration: none;
        }

        .chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 8px;
            border-radius: 999px;
            background: rgba(228,242,255,0.9);
            font-size: 0.75rem;
            color: var(--muted-text);
        }

        .chip-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: var(--accent-green);
        }

        .admin-banner {
            font-size: 0.78rem;
            padding: 4px 8px;
            border-radius: 999px;
            border: 1px dashed rgba(120, 144, 220, 0.9);
            background: rgba(227,242,255,0.7);
        }

        .admin-list {
            margin-top: 8px;
            font-size: 0.78rem;
        }

        .admin-item {
            padding: 6px 8px;
            border-radius: 10px;
            border: 1px solid rgba(210, 220, 245, 0.9);
            background: rgba(250, 252, 255, 0.95);
            margin-bottom: 6px;
        }

        .badge-plan {
            font-size: 0.72rem;
            padding: 2px 6px;
            border-radius: 999px;
            background: rgba(227,242,255,0.9);
            color: var(--muted-text);
        }

        .badge-plan.star {
            background: rgba(255,247,230,0.9);
            color: #b36b00;
        }
    </style>
</head>
<body>
<div class="page-wrap">
    <header>
        <div class="logo">
            <div class="logo-mark">LF</div>
            <div>LogiFlow AI</div>
        </div>
        <nav>
            <a href="#what-we-do">What we do</a>
            <a href="#edge">Why us</a>
            <a href="#transformation">Before → After</a>
        </nav>
        <div class="cta-header">Nigeria's first agentic logistics intelligence</div>
    </header>

    <main>
        <section class="hero">
            <div class="hero-left">
                <div class="badge">
                    <span>New</span>
                    Nigeria's first agentic logistics intelligence platform
                </div>
                <h1>A living AI command centre for Nigerian freight and FMCG ops</h1>
                <p class="hero-subtitle">
                    LogiFlow AI watches your ports, roads, fuel, and fleet in real time, predicts what will go wrong, 
                    and acts on your behalf before the damage hits.
                </p>
                <div class="hero-highlight">
                    Think of it as a logistics war room that never sleeps, never gets tired, and never misses a signal.
                </div>
                <div class="hero-list">
                    <div class="hero-pill"><strong>Who it's for:</strong> Nigerian freight forwarders, FMCG distributors, haulage</div>
                    <div class="hero-pill"><strong>Where:</strong> Lagos · Port Harcourt · Kano · nationwide corridors</div>
                    <div class="hero-pill"><strong>Ops size:</strong> 20–200 employees · active fleet · complex routes</div>
                    <div class="hero-pill"><strong>Ops reality:</strong> Manual or semi-digital · WhatsApp-first communication</div>
                </div>
                <div class="hero-actions">
                    <a href="#audit" style="text-decoration:none;">
                        <button class="btn-primary">
                            <span>●</span>
                            Book free 60‑min Operations Audit
                        </button>
                    </a>
                    <button class="btn-ghost">
                        Watch your operation like a living command centre
                    </button>
                </div>
                <div class="trust-text">
                    No pitch. In 60 minutes we map your operation, expose the leaks, and show exactly what AI can fix.
                </div>
            </div>

            <div class="hero-right">
                <div class="panel-heading">
                    <div class="panel-title">Live intelligence snapshot</div>
                    <div class="panel-chip">Demo · Nigeria ops</div>
                </div>

                <div class="mini-grid">
                    <div class="mini-card">
                        <div class="mini-label">Active trucks</div>
                        <div class="mini-value">48 on road · 6 at port</div>
                    </div>
                    <div class="mini-card">
                        <div class="mini-label">Customer queries</div>
                        <div class="mini-value">81% handled by AI · 24/7</div>
                    </div>
                    <div class="mini-card">
                        <div class="mini-label">Risk alerts (today)</div>
                        <div class="mini-value">Port congestion · 3 risky checkpoints</div>
                    </div>
                    <div class="mini-card">
                        <div class="mini-label">Fuel & route cost</div>
                        <div class="mini-value">Live tracking · no end‑of‑month shock</div>
                    </div>
                </div>

                <div class="status-row">
                    <div class="status-pill">
                        <div class="status-pill-dot"></div>
                        Watching ports · roads · fuel · fleet in real time
                    </div>
                    <div class="status-metric">
                        Saved <strong>₦1.8M</strong> in ops leakage this month (demo)
                    </div>
                </div>

                <div class="timeline">
                    <div class="timeline-row">
                        <div class="timeline-tag">Now</div>
                        <div class="timeline-text">
                            AI detects a truck silent for 30+ seconds on Lagos–Kano corridor, cross-checks road risk, and flags a possible incident.
                        </div>
                    </div>
                    <div class="timeline-row">
                        <div class="timeline-tag">AI acts</div>
                        <div class="timeline-text">
                            Customer gets a WhatsApp update automatically, backup route is recommended, and ops is alerted only if human escalation is needed.
                        </div>
                    </div>
                    <div class="timeline-row">
                        <div class="timeline-tag">You</div>
                        <div class="timeline-text">
                            Decide in minutes, not days — with live intelligence instead of gut feel and WhatsApp chaos.
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section" id="what-we-do">
            <div class="section-title">What we do · What we sell · Who it's for</div>
            <div class="section-subtitle">
                LogiFlow AI fuses live Nigerian logistics signals into one intelligence layer, delivered as a managed service.
            </div>

            <div class="grid-3">
                <div class="card">
                    <h3>What we do</h3>
                    <p>
                        Deploy an AI intelligence system into your operation that fuses data from ports, roads, fuel markets, and your fleet, 
                        then reasons over it 24/7 to surface risks, predict delays, and automate your most expensive manual work.
                    </p>
                    <div class="pill-row">
                        <div class="pill">Ports · Apapa, Tin Can, Onne</div>
                        <div class="pill">Roads · Lagos–Kano · PH corridor</div>
                        <div class="pill">Fuel markets · volatility aware</div>
                    </div>
                </div>
                <div class="card">
                    <h3>What we sell</h3>
                    <p>
                        An agentic AI logistics intelligence platform — SaaS + consulting, delivered as a managed service. 
                        You pay monthly and get a fully running intelligence system, not a tool your team has to figure out.
                    </p>
                    <div class="pill-row">
                        <div class="pill badge-plan">Starter · ₦350k / month</div>
                        <div class="pill badge-plan star">Growth · ₦750k / month</div>
                        <div class="pill badge-plan">Enterprise · custom</div>
                    </div>
                </div>
                <div class="card">
                    <h3>Target customer</h3>
                    <p>
                        Operations leaders and owners at Nigerian freight forwarders and FMCG distributors with real logistics complexity, 
                        active fleets, and 20–200 employees. You feel the pain daily; you just need proof that a solution exists.
                    </p>
                    <div class="pill-row">
                        <div class="pill-cream pill">Head of Ops · Supply Chain Director</div>
                        <div class="pill-cream pill">FMCG distributors · haulage</div>
                        <div class="pill-cream pill">Lagos · PH · Kano</div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section" id="edge">
            <div class="section-title">Why LogiFlow AI is different</div>
            <div class="section-subtitle">
                Built for Nigerian roads, Nigerian ports, and WhatsApp‑first operations — and it acts, not just alerts.
            </div>

            <div class="grid-3">
                <div class="card">
                    <h3>Living intelligence, not dashboards</h3>
                    <p>
                        Most tools show you data after the fact. LogiFlow AI watches every signal in real time, reasons over combinations, 
                        and tells you what is about to go wrong before it does — like a logistics Palantir built for Nigeria.
                    </p>
                </div>
                <div class="card">
                    <h3>Designed for Nigerian reality</h3>
                    <p>
                        Apapa congestion, illegal checkpoints, naira volatility, and WhatsApp-first comms are not edge cases; 
                        they are the core of the product. Every workflow assumes chaos, not clean ERP data.
                    </p>
                </div>
                <div class="card">
                    <h3>Acts on your behalf</h3>
                    <p>
                        When the AI detects a risk, it does not just ping you. It updates customers on WhatsApp, 
                        flags backup routes, and only escalates to humans when genuinely needed — no extra data team required.
                    </p>
                </div>
            </div>
        </section>

        <section class="section" id="transformation">
            <div class="section-title">The transformation · Before → After LogiFlow AI</div>
            <div class="section-subtitle">
                From gut feel and WhatsApp chaos to a calm, always‑on command centre.
            </div>

            <div class="compare">
                <div class="card compare-block">
                    <h4>Before LogiFlow AI</h4>
                    <div class="compare-item">
                        <div class="compare-icon bad"></div>
                        <div>Driver goes silent; nobody knows for hours.</div>
                    </div>
                    <div class="compare-item">
                        <div class="compare-icon bad"></div>
                        <div>Ops manager spends 3–5 hours daily on WhatsApp updates.</div>
                    </div>
                    <div class="compare-item">
                        <div class="compare-icon bad"></div>
                        <div>Decisions made on gut feel and old reports.</div>
                    </div>
                    <div class="compare-item">
                        <div class="compare-icon bad"></div>
                        <div>Fuel and route costs only visible at month-end.</div>
                    </div>
                    <div class="compare-item">
                        <div class="compare-icon bad"></div>
                        <div>Customers call 20 times for one update; trust erodes.</div>
                    </div>
                </div>
                <div class="card compare-block">
                    <h4>After LogiFlow AI</h4>
                    <div class="compare-item">
                        <div class="compare-icon good"></div>
                        <div>Silent truck flagged within 30 seconds — risk surfaced instantly.</div>
                    </div>
                    <div class="compare-item">
                        <div class="compare-icon good"></div>
                        <div>Roughly 81% of customer queries handled autonomously, 24/7.</div>
                    </div>
                    <div class="compare-item">
                        <div class="compare-icon good"></div>
                        <div>Decide in minutes, not days, with live intelligence.</div>
                    </div>
                    <div class="compare-item">
                        <div class="compare-icon good"></div>
                        <div>Fuel and route risk visible live — no end‑of‑month surprises.</div>
                    </div>
                    <div class="compare-item">
                        <div class="compare-icon good"></div>
                        <div>Customers receive proactive updates; trust and retention grow.</div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section" id="objections">
            <div class="section-title">Common objections · How we answer</div>
            <div class="section-subtitle">
                Your peers have asked these questions already — here is how the model is designed to respond.
            </div>

            <div class="objections-grid">
                <div class="card">
                    <div class="objection-title">“We’ve been burned by vendors before.”</div>
                    <div class="objection-q">Paid, got nothing, and ops did not change.</div>
                    <div class="objection-a">
                        You start with a free 60‑minute audit and then, if it makes sense, a 3‑month pilot at 50% off. 
                        You only pay full price after you have seen it work on your own operation. Risk sits with us, not you.
                    </div>
                </div>
                <div class="card">
                    <div class="objection-title">“₦350k per month is too expensive.”</div>
                    <div class="objection-q">Ops team already under pressure; budgets tight.</div>
                    <div class="objection-a">
                        One ops manager spending 4 hours daily on WhatsApp updates costs more than ₦1.2M per month in lost productivity alone — 
                        before counting delays, lost clients, or bad route decisions. The goal is for LogiFlow AI to pay for itself before week three.
                    </div>
                </div>
                <div class="card">
                    <div class="objection-title">“Our ops are too messy for AI.”</div>
                    <div class="objection-q">Signals are scattered, mostly WhatsApp, spreadsheets, and calls.</div>
                    <div class="objection-a">
                        The product is deliberately built for Nigerian chaos. Apapa congestion, illegal checkpoints, and WhatsApp‑first workflows are 
                        exactly what the models are tuned on — your ops do not have to be clean first.
                    </div>
                </div>
                <div class="card">
                    <div class="objection-title">“We don’t have time to implement.”</div>
                    <div class="objection-q">Operations team is already at full capacity.</div>
                    <div class="objection-a">
                        You do not implement a tool. The team maps your workflows, integrates your data, and trains your staff. 
                        The target is to get you live in about 4 weeks, with your ops manager getting time back from day one.
                    </div>
                </div>
                <div class="card">
                    <div class="objection-title">“I need to see it working first.”</div>
                    <div class="objection-q">No commitment until results are visible.</div>
                    <div class="objection-a">
                        That is the purpose of the Operations Audit and pilot — your real operation, your real data, 
                        and a clear yes/no point after you see the outputs. If it is not a fit, you walk away with clarity anyway.
                    </div>
                </div>
            </div>
        </section>

        <section class="section audit-section" id="audit">
            <div class="audit-copy">
                <div class="section-title">Book a free 60‑minute Operations Audit</div>
                <div class="section-subtitle">
                    No pitch. In one focused working session we map your operation, quantify the leaks, and show where AI unlocks the most value.
                </div>
                <p>
                    This session is designed for operators who already feel the pain of:
                </p>
                <ul>
                    <li>Trucks going dark for hours with no reliable explanation</li>
                    <li>Customer service running on endless WhatsApp threads</li>
                    <li>Fuel and route costs only visible after the month closes</li>
                    <li>Ports and checkpoints turning into silent capital traps</li>
                </ul>
                <p>
                    At the end of the call you will either see a clear AI‑powered path to reclaim lost margin and time,
                    or you walk away with a sharper map of your operation — no commitment required.
                </p>
                <div class="chip">
                    <div class="chip-dot"></div>
                    Limited pilot slots each quarter · Lagos, Port Harcourt, Kano
                </div>
            </div>

            <div class="form-card">
                <div class="form-header">
                    <h3>Request your free audit</h3>
                    <p>Share a few details about your operation. The team will follow up with suggested time slots.</p>
                </div>
                <form method="POST" action="{{ url_for('book_audit') }}">
                    <div class="field-row">
                        <div class="field">
                            <label for="name">Your name</label>
                            <input type="text" id="name" name="name" placeholder="e.g. Head of Operations" required>
                        </div>
                        <div class="field">
                            <label for="role">Role</label>
                            <input type="text" id="role" name="role" placeholder="Head of Ops, CEO, Logistics Manager" required>
                        </div>
                    </div>

                    <div class="field-row">
                        <div class="field">
                            <label for="company">Company</label>
                            <input type="text" id="company" name="company" placeholder="Company name" required>
                        </div>
                        <div class="field">
                            <label for="city">Primary corridor / city</label>
                            <input type="text" id="city" name="city" placeholder="Lagos, PH, Kano, etc.">
                        </div>
                    </div>

                    <div class="field-row">
                        <div class="field">
                            <label for="email">Work email</label>
                            <input type="email" id="email" name="email" placeholder="you@company.com" required>
                        </div>
                        <div class="field">
                            <label for="phone">WhatsApp number</label>
                            <input type="tel" id="phone" name="phone" placeholder="+234..." required>
                        </div>
                    </div>

                    <div class="field-row">
                        <div class="field">
                            <label for="employees">Team size</label>
                            <select id="employees" name="employees">
                                <option value="">Select</option>
                                <option value="under-20">Under 20</option>
                                <option value="20-50">20–50</option>
                                <option value="50-100">50–100</option>
                                <option value="100-200">100–200</option>
                                <option value="200-plus">200+</option>
                            </select>
                        </div>
                        <div class="field">
                            <label for="fleet">Fleet size (approx.)</label>
                            <input type="text" id="fleet" name="fleet" placeholder="e.g. 15 trucks">
                        </div>
                    </div>

                    <div class="field">
                        <label for="biggest_pain">Biggest pain point right now</label>
                        <textarea id="biggest_pain" name="biggest_pain" placeholder="Where does logistics hurt the most today?"></textarea>
                    </div>

                    <div class="field">
                        <label for="goal">If the audit is a success, what changes in 90 days?</label>
                        <textarea id="goal" name="goal" placeholder="Fewer lost trucks, fewer customer complaints, lower fuel leakage, etc."></textarea>
                    </div>

                    <div class="form-footer">
                        <button class="btn-primary" type="submit">
                            <span>→</span>
                            Submit audit request
                        </button>
                        <div class="form-note">
                            You will receive an email / WhatsApp follow‑up within one working day with a proposed time slot.
                        </div>
                    </div>
                </form>

                {% if audit_requests %}
                <div class="admin-banner" style="margin-top:10px;">
                    Demo only: {{ audit_requests|length }} audit request(s) captured in memory.
                    Reloading the Repl clears this.
                </div>
                <div class="admin-list">
                    {% for a in audit_requests %}
                    <div class="admin-item">
                        <strong>{{ a.name }}</strong> · {{ a.role }} at {{ a.company }} ({{ a.city or "N/A" }})<br>
                        Email: {{ a.email }} · WhatsApp: {{ a.phone }} · Team: {{ a.employees or "N/A" }} · Fleet: {{ a.fleet or "N/A" }}<br>
                        Pain: {{ a.biggest_pain or "N/A" }}<br>
                        90‑day goal: {{ a.goal or "N/A" }}
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
        </section>
    </main>

    <footer>
        <div>© {{ year }} LogiFlow AI · Agentic logistics intelligence for Nigerian freight and FMCG.</div>
        <div>
            <a href="#what-we-do">Product</a> · 
            <a href="#audit">Free audit</a>
        </div>
    </footer>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    from datetime import datetime
    year = datetime.now().year
    return render_template_string(
        PAGE_TEMPLATE,
        year=year,
        audit_requests=audit_requests
    )

@app.route("/book-audit", methods=["POST"])
def book_audit():
    data = {
        "name": request.form.get("name", "").strip(),
        "role": request.form.get("role", "").strip(),
        "company": request.form.get("company", "").strip(),
        "city": request.form.get("city", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "employees": request.form.get("employees", "").strip(),
        "fleet": request.form.get("fleet", "").strip(),
        "biggest_pain": request.form.get("biggest_pain", "").strip(),
        "goal": request.form.get("goal", "").strip(),
    }
    audit_requests.append(type("AuditRequest", (), data))
    return redirect(url_for("home"))

if __name__ == "__main__":
    # For Replit
    app.run(host="0.0.0.0", port=8000, debug=True)
