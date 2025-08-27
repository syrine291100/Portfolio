# app.py — Portfolio multipage (nav pastel chic, pages, projets sans images)
import streamlit as st
from pathlib import Path
from PIL import Image
from datetime import datetime
import csv
import smtplib, ssl
from email.message import EmailMessage


# ---------------- CONFIG ----------------
st.set_page_config(page_title="Portfolio – Syrine Chehairi", page_icon="✨", layout="wide")

PALETTE = {
    "bg": "#F8FAFC",
    "card": "#FFFFFF",
    "accent": "#A78BFA",
    "accent2": "#60A5FA",
    "accent3": "#34D399",
    "peach": "#FBCFE8",
    "text": "#0F172A",
    "muted": "#64748B",
    "border": "#E5E7EB",
}

ASSETS = Path("assets")
ASSETS.mkdir(exist_ok=True)

# ---------------- CSS -------------------
st.markdown(f"""
<style>
  :root {{
    --bg: {PALETTE["bg"]};
    --card: {PALETTE["card"]};
    --text: {PALETTE["text"]};
    --muted: {PALETTE["muted"]};
    --border: {PALETTE["border"]};
    --violet: {PALETTE["accent"]};
    --blue: {PALETTE["accent2"]};
    --green: {PALETTE["accent3"]};
    --peach: {PALETTE["peach"]};
  }}
  .stApp {{
    background: var(--bg);
    color: var(--text);
    font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "Helvetica Neue", Arial;
  }}

  /* NAVBAR — verre dépoli pastel + chips compactes */
  .navbar {{
    position: sticky; top: 0; z-index: 999;
    margin: 6px 0 10px 0;
    padding: 10px 14px;
    border-radius: 14px;
    border: 1px solid var(--border);
    background: linear-gradient(120deg, #ffffffE6, #ffffffCC);
    backdrop-filter: blur(8px);
    box-shadow: 0 6px 20px rgba(15,23,42,0.06);
  }}
  .nav-inner {{
    display: flex; align-items: center; gap: 10px;
  }}
  .brand {{
    font-weight: 750; color: var(--text);
    margin-right: 6px; white-space: nowrap;
  }}
  .brand-sub {{
    color: var(--muted); white-space: nowrap;
  }}
  .nav-menu {{
    display: flex; gap: 8px; margin-left: auto;
    overflow-x: auto; -webkit-overflow-scrolling: touch;
    padding-bottom: 4px;
  }}
  .nav-chip {{
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 14px;
    border-radius: 999px;
    border: 1px solid var(--border);
    color: var(--text);
    background: linear-gradient(180deg, #fff, #f7faff);
    text-decoration: none;
    font-weight: 600; font-size: .94rem;
    white-space: nowrap;
    box-shadow: 0 1px 0 #fff inset, 0 2px 8px rgba(15,23,42,.04);
    transition: transform .12s ease, box-shadow .2s ease, border-color .2s ease;
  }}
  .nav-chip:hover {{
    transform: translateY(-1px);
    box-shadow: 0 8px 16px rgba(15,23,42,.10);
    border-color: #cdd7e5;
  }}
  .nav-chip.active {{
    background: linear-gradient(120deg, #EDE9FE, #DBEAFE);
    border-color: #c7d2fe;
    box-shadow: 0 10px 22px rgba(99,102,241,.25);
  }}
  .nav-emoji {{ font-size: 1.05rem; }}

  /* HERO / CARDS */
  .top-hero {{
    background: linear-gradient(120deg, #EDE9FE55, #DBEAFE55);
    border: 1px solid var(--border);
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
    margin: 12px 0 18px 0;
  }}
  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(15,23,42,0.05);
    margin-bottom: 14px;
  }}
  .section-title {{
    color: var(--text);
    border-left:6px solid var(--blue);
    padding-left:10px;
    margin: 8px 0 14px 0;
  }}
  .pill {{
    display:inline-block;
    padding: 6px 10px;
    margin: 4px 6px 0 0;
    border-radius: 999px;
    background: #ECFDF555;
    color: var(--text);
    border: 1px solid #D1FAE5;
    font-size: .88rem;
    white-space: nowrap;
  }}
  .muted {{ color: var(--muted); }}
</style>
""", unsafe_allow_html=True)


# ---------------- UTILS ------------------
def send_mail(name, sender_email, subject, body):
    host = st.secrets["EMAIL_HOST"]
    port = int(st.secrets.get("EMAIL_PORT", 587))
    user = st.secrets["EMAIL_USER"]
    pwd  = st.secrets["EMAIL_PASS"]
    to   = st.secrets.get("EMAIL_TO", user)

    msg = EmailMessage()
    msg["Subject"] = f"[Portfolio] {subject} — {name}"
    msg["From"]    = user
    msg["To"]      = to
    msg["Reply-To"]= sender_email
    msg.set_content(f"""Nouveau message reçu depuis le portfolio:

Nom: {name}
Email: {sender_email}
Sujet: {subject}

{body}
""")

    ctx = ssl.create_default_context()
    with smtplib.SMTP(host, port) as server:
        server.starttls(context=ctx)
        server.login(user, pwd)
        server.send_message(msg)

def load_img(path: Path):
    return Image.open(path) if path.exists() else None

def section_title(label: str):
    st.markdown(f"## <span class='section-title'>{label}</span>", unsafe_allow_html=True)

def get_page_from_query():
    """Récupère ?page=... en restant robuste au format de PAGES."""
    try:
        qp = st.query_params
        page = qp.get("page", "home")
        if isinstance(page, list):
            page = page[0] if page else "home"
    except Exception:
        qp = st.experimental_get_query_params()
        page = qp.get("page", ["home"])[0]
    keys = [p[0] for p in PAGES]  # <-- FIX: on ne suppose pas 2 éléments
    return page if page in keys else "home"

# ---------------- NAV DATA ----------------
PAGES = [
    ("home",      "🏠", "Accueil"),
    ("skills",    "🧩", "Compétences"),
    ("projects",  "📂", "Projets"),
    ("experience","💼", "Expériences"),
    ("education", "🎓", "Formations"),
    ("contact",   "✉️", "Contact"),
    ("message",   "📝", "Me contacter"),
]
current_page = get_page_from_query()

# ---------------- NAVBAR (TOP) -----------
nav_items = []
for key, emoji, label in PAGES:
    active = " active" if key == current_page else ""
    nav_items.append(f"<a class='nav-chip{active}' href='?page={key}' target='_self'>{emoji} {label}</a>")
st.markdown(
    "<div class='navbar'><div class='nav-inner'>"
    "<div><div class='brand'>Syrine&nbsp;Chehairi</div><div class='brand-sub'>Portfolio</div></div>"
    f"<div class='nav-menu'>{''.join(nav_items)}</div>"
    "</div></div>",
    unsafe_allow_html=True,
)

# ---------------- HERO -------------------
with st.container():
    st.markdown("<div class='top-hero'>", unsafe_allow_html=True)
    c1, c2 = st.columns([3,1])
    with c1:
        st.markdown("# **Syrine Chehairi**")
        st.caption("Ingénieure informatique – Data / IA / Software • SupGalilée 2025")
        st.markdown("Environnements **réglementés** & **projets critiques (V&V)**. Je livre **vite**, **proprement** et **en équipe**.")
    with c2:
        photo = load_img(ASSETS / "photo.jpg")
        if photo:
            st.image(photo, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PAGES -------------------
def page_home():
    section_title("Aperçu rapide")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='card'><b>Ce que je fais</b><br>- Data & ML (Python, SQL, Monte Carlo)<br>- Dev logiciel / Backend / Full-Stack<br>- Méthodes V&V, tests, doc, formation</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'><b>Ce que j’aime</b><br>- Résoudre des problèmes concrets<br>- Travailler proprement & expliquer<br>- Apprendre vite, partager</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='card'><b>Ce que je cherche</b><br>- Data Engineer / ML Engineer<br>- Software/Backend Engineer<br>- En France (sur site ou remote) • CDI</div>", unsafe_allow_html=True)

def page_skills():
    section_title("Compétences")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**Langages**")
    for s in ["Python", "Java", "C/C++", "JavaScript", "SQL", "PHP", "Julia", "Bash"]:
        st.markdown(f"<span class='pill'>{s}</span>", unsafe_allow_html=True)
    st.markdown("<br><br>**Frameworks & libs**", unsafe_allow_html=True)
    for s in ["Django", "React (bases)", "TensorFlow (bases)", "PyTest", "NumPy", "Pandas", "Matplotlib"]:
        st.markdown(f"<span class='pill'>{s}</span>", unsafe_allow_html=True)
    st.markdown("<br><br>**Data / HPC**", unsafe_allow_html=True)
    for s in ["Méthode Monte Carlo", "CUDA (bases GPU)", "Excel avancé", "Git"]:
        st.markdown(f"<span class='pill'>{s}</span>", unsafe_allow_html=True)
    st.markdown("<br><br>**Systèmes / Cloud**", unsafe_allow_html=True)
    for s in ["Linux", "Windows", "Docker", "CI/CD (léger)"]:
        st.markdown(f"<span class='pill'>{s}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def page_projects():
    section_title("Projets")
    projects = [
        {
            "title": "Outil Monte Carlo (Edvance)",
            "bullets": [
                "Simulation d’incertitudes en Python (méthode Monte Carlo).",
                "Optimisation des performances (vectorisation / bases GPU).",
                "Tests automatisés (PyTest), documentation et ateliers utilisateurs.",
                "Contexte V&V : traçabilité, qualité, exigences."
            ],
            "stack": ["Python", "NumPy", "PyTest", "Git"]
        },
        {
            "title": "App web Herbier (> 6M images)",
            "bullets": [
                "Pipeline ETL et stockage massif d’images.",
                "Architecture, coordination d’équipe et restitution scientifique.",
                "Mise à l’échelle et gestion des flux."
            ],
            "stack": ["Python", "ETL", "SQL", "Docker"]
        },
        {
            "title": "Visualisation fermetures de routes – DIRIF",
            "bullets": [
                "Mise en données, ergonomie d’interface et data viz.",
                "Outil opérationnel pour équipes terrain (filtres, export, lecture rapide)."
            ],
            "stack": ["Python", "Data Viz", "UX"]
        },
        {
            "title": "Programmation parallèle (C/CUDA) – Ondes",
            "bullets": [
                "Simulation de propagation d’ondes (HPC).",
                "Mesures et comparaison de performances (multi-thread / GPU)."
            ],
            "stack": ["C", "CUDA", "HPC", "Linux"]
        },
    ]
    for p in projects:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {p['title']}")
        for b in p["bullets"]:
            st.write(f"- {b}")
        if p.get("stack"):
            st.markdown("<br><span class='muted'>Technos :</span> ", unsafe_allow_html=True)
            for tag in p["stack"]:
                st.markdown(f"<span class='pill'>{tag}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def page_experience():
    section_title("Expériences")
    exp = [
        ("2024–2025", "Ingénieure stagiaire – Edvance (EDF)",
         "Outil Python Monte Carlo, optimisation perf, tests PyTest, doc, formation utilisateurs, V&V."),
        ("2023", "Développeuse – DIRIF",
         "Visualisation fermetures de routes : données, ergonomie, data viz, restitution terrain."),
        ("2022", "Stagiaire – Speakeasy",
         "Plateforme e-learning (auth, streaming, stockage) ; cycle complet produit."),
        ("2019–2022", "Tutrice & encadrement pédagogique – Sorbonne Paris Nord",
         "Tutorat L0/L1 (maths / info C) ; encadrement L2 (projet Java)."),
        ("2021–2024", "Cheffe de rang – Fratellini Caffè",
         "Coordination équipe et gestion opérationnelle (cadre exigeant)."),
    ]
    for d, r, desc in exp:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"**{d} — {r}**")
        st.caption(desc)
        st.markdown("</div>", unsafe_allow_html=True)

def page_education():
    section_title("Formations")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**Diplôme d’ingénieure – spécialité Informatique (SupGalilée), 2025**")
    st.caption("Projet de fin d’études, projets logiciels, data/ML, HPC.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("**Double licence Mathématiques & Informatique – Sorbonne Paris Nord, 2022**")
    st.caption("Algo, statistiques, structures de données, Java/C, bases solides.")
    st.markdown("</div>", unsafe_allow_html=True)

def page_contact():
    section_title("Contact")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("📧 syrine.chehairi@hotmail.com")
    st.write("📱 06 99 87 97 04")
    st.link_button("🔗 LinkedIn", "https://www.linkedin.com/in/syrine-chehairi-866099184/", use_container_width=True)
    st.link_button("💻 GitHub", "https://github.com/syrine291100", use_container_width=True)
    cv_file = ASSETS / "CV_Syrine_Chehairi.pdf"
    if cv_file.exists():
        with open(cv_file, "rb") as f:
            st.download_button("📄 Télécharger mon CV", f, file_name=cv_file.name, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def page_message():
    section_title("Me contacter directement")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.caption("Remplissez ce formulaire : vos messages sont enregistrés dans un fichier local (messages.csv).")
    with st.form("contact_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Votre nom *")
        with col2:
            email = st.text_input("Votre email *")
        subject = st.text_input("Sujet *")
        message = st.text_area("Message *", height=160)
        send = st.form_submit_button("Envoyer ✅")
        if send:
            if not (name and email and subject and message):
                st.error("Merci de compléter tous les champs obligatoires.")
            else:
                # 1) Envoi par e-mail
                try:
                    send_mail(name, email, subject, message)
                    st.success("Message envoyé par e-mail ✅")
                except Exception as e:
                    st.warning(f"Impossible d'envoyer par e-mail (fallback CSV). Détail: {e}")

                # 2) Sauvegarde locale en CSV (fallback / audit)
                out = Path("messages.csv")
                file_exists = out.exists()
                with out.open("a", newline="", encoding="utf-8") as f:
                    import csv
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["timestamp", "name", "email", "subject", "message"])
                    from datetime import datetime
                    writer.writerow([datetime.now().isoformat(), name, email, subject, message])
                st.info("Message archivé dans messages.csv 📄")

           st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ROUTER -----------------
ROUTES = {
    "home": page_home,
    "skills": page_skills,
    "projects": page_projects,
    "experience": page_experience,
    "education": page_education,
    "contact": page_contact,
    "message": page_message,
}
ROUTES.get(current_page, page_home)()
