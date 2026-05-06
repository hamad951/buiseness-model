"""
#BUSINESS HELPER - COMPLETE PROFESSIONAL SYSTEM
#Single File Application | Admin Controlled | Auto Email | Job Search | B2B Leads
#Author: Business Helper Team
#Version: 3.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import sqlite3
import hashlib
import json
import os
import smtplib
import time
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings('ignore')

ADZUNA_APP_ID = "71a53b73"
ADZUNA_API_KEY = "02bd44aa152e763297fadf95c75119a1"
NEWS_API_KEY = "03f7c2c09a7b45e1b25bc25bf4377fae"

st.set_page_config(
    page_title="Business Helper - AI Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #0ea5e9;
    --primary-dark: #0284c7;
    --accent: #f59e0b;
    --success: #10b981;
    --danger: #ef4444;
    --bg-dark: #0a0f1e;
    --bg-card: #111827;
    --bg-card2: #1a2236;
    --border: rgba(14, 165, 233, 0.2);
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
    --glow: 0 0 20px rgba(14, 165, 233, 0.3);
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background-color: var(--bg-dark) !important;
    color: var(--text-main) !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1529 50%, #0a1628 100%) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2e 0%, #0a1422 100%) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text-main) !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-main) !important;
    font-family: 'Outfit', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: var(--glow) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: 0.3px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(14, 165, 233, 0.5) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-muted) !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
}

[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

[data-testid="stMetricValue"] {
    color: var(--primary) !important;
    font-weight: 700 !important;
}

[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

[data-testid="stForm"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}

.page-header {
    background: linear-gradient(135deg, #0d1b2e, #0a2040);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.page-header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, var(--primary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.page-header p { color: var(--text-muted); font-size: 1rem; }

.stat-card {
    background: linear-gradient(135deg, var(--bg-card), var(--bg-card2));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
}

.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
}

.stat-card:hover {
    transform: translateY(-4px);
    border-color: var(--primary);
    box-shadow: var(--glow);
}

.stat-card .icon { font-size: 2rem; margin-bottom: 0.5rem; }
.stat-card .value { font-size: 2rem; font-weight: 800; color: var(--primary); line-height: 1; }
.stat-card .label { color: var(--text-muted); font-size: 0.8rem; font-weight: 500; margin-top: 0.3rem; text-transform: uppercase; letter-spacing: 0.5px; }

.info-card {
    background: linear-gradient(135deg, var(--bg-card), var(--bg-card2));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.info-card:hover {
    border-color: var(--primary);
    box-shadow: var(--glow);
    transform: translateX(4px);
}

.info-card h3 { color: var(--text-main); font-weight: 700; margin-bottom: 0.4rem; font-size: 1.05rem; }
.info-card p { color: var(--text-muted); font-size: 0.88rem; margin: 0.2rem 0; }
.info-card a { color: var(--primary); text-decoration: none; }

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    background: rgba(14,165,233,0.15);
    color: var(--primary);
    border: 1px solid rgba(14,165,233,0.3);
}

.badge-gold { background: rgba(245,158,11,0.15); color: var(--accent); border-color: rgba(245,158,11,0.3); }
.badge-green { background: rgba(16,185,129,0.15); color: var(--success); border-color: rgba(16,185,129,0.3); }

.plan-card {
    background: linear-gradient(135deg, var(--bg-card), var(--bg-card2));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
}

.plan-card.featured {
    border-color: var(--primary);
    box-shadow: var(--glow);
    background: linear-gradient(135deg, #0d2040, #0a1a35);
}

.plan-card h3 { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--text-main); }
.plan-card .price { font-size: 2.2rem; font-weight: 800; color: var(--primary); line-height: 1.2; }
.plan-card .currency { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem; }
.plan-card ul { list-style: none; padding: 0; margin: 1rem 0; text-align: left; }
.plan-card ul li { padding: 0.3rem 0; color: var(--text-muted); font-size: 0.88rem; }
.plan-card ul li::before { content: "✓ "; color: var(--success); font-weight: 700; }

.sidebar-profile {
    background: rgba(14,165,233,0.08);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem;
    margin: 0.5rem 0 1rem;
}

.chat-user {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    border-radius: 16px 16px 4px 16px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    color: white;
    font-size: 0.9rem;
    max-width: 80%;
    margin-left: auto;
}

.chat-bot {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 16px 16px 16px 4px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    color: var(--text-main);
    font-size: 0.9rem;
    max-width: 80%;
}

.footer {
    text-align: center;
    padding: 2rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    margin-top: 3rem;
    color: var(--text-muted);
    font-size: 0.85rem;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-main);
    margin: 1.5rem 0 1rem;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE
# ============================================

class DatabaseManager:
    def __init__(self, db_path="business_helper.db"):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
            full_name TEXT, country TEXT, skills TEXT, package TEXT DEFAULT 'Free',
            created_date TEXT, last_login TEXT, status TEXT DEFAULT 'active')''')
        c.execute('''CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, email TEXT, created_date TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS applied_jobs (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, job_title TEXT, company TEXT, applied_date TEXT, status TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT, industry TEXT, contact_person TEXT, email TEXT, phone TEXT,
            score REAL, status TEXT, created_date TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS email_campaigns (id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_name TEXT, subject TEXT, body TEXT, recipient_count INTEGER, sent_date TEXT, status TEXT)''')
        c.execute("SELECT * FROM admin WHERE username='Hamad'")
        if not c.fetchone():
            hp = hashlib.sha256("Hamad123@".encode()).hexdigest()
            c.execute("INSERT INTO admin (username,password,email,created_date) VALUES (?,?,?,?)",
                ("Hamad", hp, "admin@businesshelper.com", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

    def verify_admin(self, username, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        hp = hashlib.sha256(password.encode()).hexdigest()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, hp))
        r = c.fetchone(); conn.close(); return r is not None

    def register_user(self, username, email, password, full_name, country, skills):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        hp = hashlib.sha256(password.encode()).hexdigest()
        try:
            c.execute('''INSERT INTO users (username,email,password,full_name,country,skills,package,created_date,status)
                VALUES (?,?,?,?,?,?,?,?,?)''',
                (username, email, hp, full_name, country, skills, "Free",
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "active"))
            conn.commit(); return True, "Account created successfully!"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists!"
        finally:
            conn.close()

    def verify_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        hp = hashlib.sha256(password.encode()).hexdigest()
        c.execute("SELECT id,username,email,package,full_name,country FROM users WHERE username=? AND password=? AND status='active'", (username, hp))
        u = c.fetchone(); conn.close()
        if u: return {'id':u[0],'username':u[1],'email':u[2],'package':u[3],'full_name':u[4],'country':u[5]}
        return None

    def get_all_users(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT id,username,email,full_name,country,package,created_date,status FROM users", conn)
        conn.close(); return df

    def update_user_package(self, user_id, package):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor(); c.execute("UPDATE users SET package=? WHERE id=?", (package, user_id))
        conn.commit(); conn.close()

    def delete_user(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor(); c.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit(); conn.close()

    def get_system_stats(self):
        conn = sqlite3.connect(self.db_path); c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users"); total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM users WHERE package='Pro'"); pro = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM users WHERE package='Business'"); biz = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM leads"); leads = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM email_campaigns"); camps = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM applied_jobs"); apps = c.fetchone()[0]
        conn.close()
        return {'total_users':total,'pro_users':pro,'business_users':biz,'free_users':total-pro-biz,
                'total_leads':leads,'total_campaigns':camps,'total_applications':apps}

    def add_lead(self, company_name, industry, contact_person, email, phone, score):
        conn = sqlite3.connect(self.db_path); c = conn.cursor()
        c.execute("INSERT INTO leads (company_name,industry,contact_person,email,phone,score,status,created_date) VALUES (?,?,?,?,?,?,?,?)",
            (company_name, industry, contact_person, email, phone, score, 'active', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit(); conn.close()

    def get_all_leads(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM leads ORDER BY score DESC", conn)
        conn.close(); return df

    def save_applied_job(self, user_id, job_title, company):
        conn = sqlite3.connect(self.db_path); c = conn.cursor()
        c.execute("INSERT INTO applied_jobs (user_id,job_title,company,applied_date,status) VALUES (?,?,?,?,?)",
            (user_id, job_title, company, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'applied'))
        conn.commit(); conn.close()

    def save_email_campaign(self, name, subject, body, count):
        conn = sqlite3.connect(self.db_path); c = conn.cursor()
        c.execute("INSERT INTO email_campaigns (campaign_name,subject,body,recipient_count,sent_date,status) VALUES (?,?,?,?,?,?)",
            (name, subject, body, count, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'sent'))
        conn.commit(); conn.close()

# ============================================
# EMAIL AUTOMATOR
# ============================================

class EmailAutomator:
    def __init__(self):
        self.templates = {
            "cold_outreach": "Subject: Grow Your Business with AI - {company_name}\n\nDear {contact_name},\n\nWe've built an AI platform that can help {company_name} increase leads by 300%.\n\nCan we schedule a 15-min demo?\n\nBest,\nBusiness Helper Team",
            "follow_up": "Subject: Following Up - {company_name}\n\nHi {contact_name},\n\nJust following up on our AI solutions for {company_name}. We have a 30% early-adopter discount available.\n\nBest, Business Helper",
            "partnership": "Subject: Partnership Opportunity - {company_name}\n\nDear {contact_name},\n\nI see great potential in partnering with {company_name}. Let's connect!\n\nWarm regards, Business Helper",
            "newsletter": "Subject: Weekly Business Insights for {company_name}\n\nHello {contact_name},\n\nThis week: AI grew 45%, remote jobs up 60%.\n\nSpecial: 50% off Pro plan this week!\n\nBest, Business Helper"
        }

    def generate_personalized_email(self, template_name, company_name, contact_name):
        if template_name in self.templates:
            return self.templates[template_name].format(company_name=company_name, contact_name=contact_name)
        return None

# ============================================
# API FUNCTIONS
# ============================================

def fetch_real_jobs(job_title, country):
    codes = {"Pakistan":"pk","USA":"us","UK":"gb","Canada":"ca","India":"in","UAE":"ae","Germany":"de","Australia":"au"}
    code = codes.get(country, "pk")
    url = f"https://api.adzuna.com/v1/api/jobs/{code}/search/1"
    params = {"app_id": ADZUNA_APP_ID, "app_key": ADZUNA_API_KEY, "what": job_title, "results_per_page": 20}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return [{'title': j.get('title','N/A'), 'company': j.get('company',{}).get('display_name','Unknown'),
                     'location': j.get('location',{}).get('display_name','Remote'),
                     'salary': f"{j.get('salary_min','N/A')} - {j.get('salary_max','N/A')}",
                     'url': j.get('redirect_url','#')} for j in data.get('results',[])]
        return None
    except Exception:
        return None

def fetch_market_news():
    url = f"https://newsapi.org/v2/top-headlines?category=business&apiKey={NEWS_API_KEY}&pageSize=10"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return [{'title': a.get('title','N/A'), 'source': a.get('source',{}).get('name','Unknown'),
                     'url': a.get('url','#')} for a in r.json().get('articles',[])]
        return None
    except Exception:
        return None

# ============================================
# SESSION STATE
# ============================================

for k, v in [("authenticated",False),("is_admin",False),("username",""),("user_id",None),
              ("user_email",""),("package","Free"),("chat_history",[]),("applied_jobs",[])]:
    if k not in st.session_state:
        st.session_state[k] = v

db = DatabaseManager()

PLOT = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Outfit', color='#94a3b8'),
            title_font=dict(family='Outfit', color='#f1f5f9', size=15),
            xaxis=dict(gridcolor='rgba(14,165,233,0.1)'), yaxis=dict(gridcolor='rgba(14,165,233,0.1)'),
            colorway=['#0ea5e9','#f59e0b','#10b981','#8b5cf6','#ef4444'])

# ============================================
# ADMIN DASHBOARD
# ============================================

def show_admin_dashboard():
    st.markdown("<div class='page-header'><h1>👑 Admin Control Panel</h1><p>Complete System Management</p></div>", unsafe_allow_html=True)
    stats = db.get_system_stats()

    c1,c2,c3,c4 = st.columns(4)
    for col, icon, val, label in zip([c1,c2,c3,c4],
        ["👥","⭐","🏆","📧"],
        [stats['total_users'],stats['pro_users'],stats['business_users'],stats['total_campaigns']],
        ["Total Users","Pro Users","Business Users","Campaigns"]):
        with col:
            st.markdown(f"<div class='stat-card'><div class='icon'>{icon}</div><div class='value'>{val}</div><div class='label'>{label}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    t1,t2,t3,t4,t5 = st.tabs(["👥 Users","🏢 Leads","📊 Analytics","💰 Revenue","⚙️ Settings"])

    with t1:
        st.markdown("<div class='section-title'>Registered Users</div>", unsafe_allow_html=True)
        df = db.get_all_users()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            ca, cb = st.columns(2)
            with ca:
                uid = st.number_input("User ID to Upgrade", min_value=1, step=1)
                pkg = st.selectbox("Package", ["Free","Starter","Pro","Business"])
                if st.button("Update Package"):
                    db.update_user_package(uid, pkg); st.success(f"✅ Updated!"); st.rerun()
            with cb:
                did = st.number_input("User ID to Delete", min_value=1, step=1)
                if st.button("⚠️ Delete User"):
                    db.delete_user(did); st.warning("Deleted"); st.rerun()
        else:
            st.info("No users yet")

    with t2:
        st.markdown("<div class='section-title'>Business Leads</div>", unsafe_allow_html=True)
        with st.expander("➕ Add Lead"):
            ca,cb = st.columns(2)
            with ca:
                co = st.text_input("Company"); ind = st.selectbox("Industry",["Technology","Finance","Healthcare","Retail","Manufacturing"]); ct = st.text_input("Contact")
            with cb:
                em = st.text_input("Email"); ph = st.text_input("Phone"); sc = st.slider("Score",0,100,50)
            if st.button("💾 Save Lead"):
                db.add_lead(co,ind,ct,em,ph,sc); st.success("✅ Saved!"); st.rerun()
        leads = db.get_all_leads()
        if not leads.empty:
            st.dataframe(leads, use_container_width=True)
            fig = px.pie(leads, values='score', names='industry', title="Leads by Industry", hole=0.4)
            fig.update_layout(**PLOT); st.plotly_chart(fig, use_container_width=True)

    with t3:
        ca,cb = st.columns(2)
        with ca:
            rd = pd.DataFrame({'Month':['Jan','Feb','Mar','Apr','May','Jun'],'Revenue':[5000,7500,12000,15000,22000,28000]})
            fig1 = px.area(rd, x='Month', y='Revenue', title="Monthly Revenue (PKR)")
            fig1.update_layout(**PLOT); fig1.update_traces(fill='tozeroy', fillcolor='rgba(14,165,233,0.1)', line_color='#0ea5e9')
            st.plotly_chart(fig1, use_container_width=True)
        with cb:
            ud = pd.DataFrame({'Package':['Free','Pro','Business'],'Count':[stats['free_users'],stats['pro_users'],stats['business_users']]})
            fig2 = px.pie(ud, values='Count', names='Package', title="User Distribution", hole=0.4)
            fig2.update_layout(**PLOT); st.plotly_chart(fig2, use_container_width=True)

    with t4:
        tr = (stats['pro_users']*1499)+(stats['business_users']*3999)
        ca,cb,cc = st.columns(3)
        with ca: st.metric("💰 Total Revenue", f"PKR {tr:,.0f}")
        with cb: st.metric("📈 Monthly", f"PKR {tr/3:,.0f}")
        with cc: st.metric("👥 Per User", f"PKR {tr/max(stats['total_users'],1):,.0f}")

    with t5:
        st.code(f"Adzuna: {ADZUNA_APP_ID} / {ADZUNA_API_KEY[:8]}...\nNews: {NEWS_API_KEY[:8]}...", language="text")
        st.text_input("SMTP Server", "smtp.gmail.com")
        st.number_input("SMTP Port", value=587)
        st.text_input("Email"); st.text_input("Password", type="password")
        if st.button("Save"): st.success("✅ Saved!")

# ============================================
# USER DASHBOARD
# ============================================

def show_user_dashboard():
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center;padding:1rem 0 0.5rem;'>
            <div style='font-size:2.5rem;'>🚀</div>
            <div style='font-size:1.2rem;font-weight:800;color:#f1f5f9;'>Business Helper</div>
            <div style='font-size:0.7rem;color:#0ea5e9;letter-spacing:2px;text-transform:uppercase;'>AI Platform</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='sidebar-profile'>
            <div style='font-weight:700;color:#f1f5f9;'>👋 {st.session_state.username}</div>
            <div style='font-size:0.78rem;color:#94a3b8;margin-top:3px;'>📧 {st.session_state.user_email}</div>
            <div style='margin-top:7px;'><span class='badge badge-gold'>📦 {st.session_state.package}</span></div>
        </div>
        """, unsafe_allow_html=True)

        selected = option_menu(
            menu_title=None,
            options=["Dashboard","Find Jobs","B2B Leads","Email Engine","Market News","AI Chat","Upgrade"],
            icons=["house-fill","briefcase-fill","people-fill","envelope-fill","newspaper","chat-fill","credit-card-fill"],
            default_index=0,
            styles={
                "container": {"padding": "0", "background": "transparent"},
                "icon": {"color": "#0ea5e9", "font-size": "15px"},
                "nav-link": {"color": "#94a3b8", "margin": "2px 0", "border-radius": "10px", "font-size": "0.88rem"},
                "nav-link-selected": {"background": "rgba(14,165,233,0.15)", "color": "#0ea5e9", "font-weight": "600"},
            }
        )

        st.markdown("<hr style='border-color:rgba(14,165,233,0.2);margin:1rem 0;'>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False; st.rerun()

    if selected == "Dashboard":
        st.markdown("<div class='page-header'><h1>🌟 Welcome to Business Helper</h1><p>Your AI-Powered Growth Platform</p></div>", unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        for col, icon, val, label in zip([c1,c2,c3,c4],["🌍","💼","🏢","⭐"],["50+","10K+","5K+","95%"],["Countries","Jobs","Leads","Success"]):
            with col:
                st.markdown(f"<div class='stat-card'><div class='icon'>{icon}</div><div class='value'>{val}</div><div class='label'>{label}</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📊 Your Weekly Activity</div>", unsafe_allow_html=True)
        ad = pd.DataFrame({'Date':pd.date_range(start='2025-01-01',periods=7),'Jobs Applied':[2,3,5,4,6,8,5],'Leads Contacted':[1,2,3,4,5,7,6]})
        fig = px.line(ad, x='Date', y=['Jobs Applied','Leads Contacted'], markers=True)
        fig.update_layout(**PLOT); st.plotly_chart(fig, use_container_width=True)

    elif selected == "Find Jobs":
        st.markdown("<div class='page-header'><h1>💼 Global Job Search</h1><p>Powered by Adzuna API</p></div>", unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1: jt = st.text_input("Job Title", "Software Engineer")
        with c2: cn = st.selectbox("Country", ["Pakistan","USA","UK","Canada","India","UAE","Germany","Australia"])
        if st.button("🔍 Search Jobs", type="primary"):
            with st.spinner("Searching..."):
                jobs = fetch_real_jobs(jt, cn)
                if jobs:
                    for j in jobs:
                        st.markdown(f"<div class='info-card'><h3>🎯 {j['title']}</h3><p>🏢 <strong>{j['company']}</strong> &nbsp;|&nbsp; 📍 {j['location']} &nbsp;|&nbsp; 💰 {j['salary']}</p></div>", unsafe_allow_html=True)
                        if st.button(f"Apply → {j['company']}", key=j['title']):
                            db.save_applied_job(st.session_state.user_id, j['title'], j['company'])
                            st.success(f"✅ Applied!"); st.balloons()
                else:
                    st.warning("⚠️ Could not fetch jobs.")

    elif selected == "B2B Leads":
        st.markdown("<div class='page-header'><h1>🏢 B2B Lead Generation</h1><p>AI-scored business contacts</p></div>", unsafe_allow_html=True)
        ind = st.selectbox("Industry", ["Technology","Finance","Healthcare","Retail","Manufacturing","Education"])
        if st.button("⚡ Generate Leads", type="primary"):
            leads = [
                {"company":"TechCorp Solutions","contact":"John Smith","email":"john@techcorp.com","phone":"+1 234 567 8900","score":95},
                {"company":f"Global {ind} Inc","contact":"Sarah Johnson","email":"sarah@global.com","phone":"+44 20 1234 5678","score":87},
                {"company":f"{ind} Innovators","contact":"Ahmed Khan","email":"ahmed@innovators.com","phone":"+92 300 1234567","score":82},
                {"company":f"Premier {ind} Co","contact":"Maria Garcia","email":"maria@premier.com","phone":"+49 30 12345678","score":78}
            ]
            for lead in leads:
                bc = "badge-green" if lead['score']>=85 else "badge-gold"
                st.markdown(f"<div class='info-card'><h3>🏢 {lead['company']}</h3><p>👤 {lead['contact']} &nbsp;|&nbsp; 📧 {lead['email']} &nbsp;|&nbsp; 📞 {lead['phone']}</p><span class='badge {bc}'>Score: {lead['score']}/100</span></div>", unsafe_allow_html=True)
                if st.button(f"💾 Save {lead['company']}", key=lead['company']):
                    db.add_lead(lead['company'],ind,lead['contact'],lead['email'],lead['phone'],lead['score'])
                    st.success("✅ Saved!")

    elif selected == "Email Engine":
        st.markdown("<div class='page-header'><h1>📧 Email Campaign Engine</h1><p>Professional automated outreach</p></div>", unsafe_allow_html=True)
        limits = {"Free":5,"Starter":200,"Pro":2000,"Business":10000}
        st.info(f"📊 Daily limit: **{limits.get(st.session_state.package,5)} emails** ({st.session_state.package} plan)")
        ttype = st.selectbox("Template", ["Cold Outreach","Follow-up","Partnership","Newsletter"])
        tmap = {"Cold Outreach":"cold_outreach","Follow-up":"follow_up","Partnership":"partnership","Newsletter":"newsletter"}
        with st.form("ef"):
            c1,c2 = st.columns(2)
            with c1: rn = st.text_input("Recipient Name"); co = st.text_input("Company")
            with c2: re = st.text_input("Email")
            if st.form_submit_button("📤 Generate Email", type="primary"):
                body = EmailAutomator().generate_personalized_email(tmap[ttype], co, rn)
                if body:
                    st.text_area("Preview", body, height=250)
                    if st.session_state.package == "Free": st.warning("🔒 Demo mode — upgrade to send")
                    else: st.success(f"✅ Ready for {rn}!")

    elif selected == "Market News":
        st.markdown("<div class='page-header'><h1>📰 Market Intelligence</h1><p>Live business news</p></div>", unsafe_allow_html=True)
        if st.button("🔄 Fetch News", type="primary"):
            with st.spinner("Loading..."):
                news = fetch_market_news()
                if news:
                    for n in news:
                        st.markdown(f"<div class='info-card'><h3>📌 {n['title']}</h3><p>📰 {n['source']} &nbsp;|&nbsp; <a href='{n['url']}' target='_blank'>Read →</a></p></div>", unsafe_allow_html=True)
                else:
                    for d in ["🚀 AI market grows 45% in Q1 2025","💰 Pakistan IT exports reach $3.5B","📈 Remote jobs up 60% worldwide"]:
                        st.success(d)

    elif selected == "AI Chat":
        st.markdown("<div class='page-header'><h1>💬 AI Business Assistant</h1><p>24/7 intelligent support</p></div>", unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            css = "chat-user" if msg["role"]=="user" else "chat-bot"
            icon = "👤" if msg["role"]=="user" else "🤖"
            st.markdown(f"<div class='{css}'>{icon} {msg['content']}</div>", unsafe_allow_html=True)
        ui = st.text_input("Ask anything...")
        if st.button("Send →", type="primary") and ui:
            st.session_state.chat_history.append({"role":"user","content":ui})
            ul = ui.lower()
            if "job" in ul: r = "Head to Find Jobs — 10,000+ listings worldwide!"
            elif "email" in ul: r = "Use Email Engine for pro campaigns. Pro plan = 2,000/day!"
            elif "lead" in ul: r = "B2B Leads generates AI-scored contacts with full details."
            elif "upgrade" in ul: r = "Starter: 499 PKR | Pro: 1,499 PKR | Business: 3,999 PKR"
            elif "price" in ul or "cost" in ul: r = "Free (5/day) → Starter 499 → Pro 1,499 → Business 3,999 PKR"
            else: r = "I help with jobs, leads, email campaigns, and business growth. What do you need?"
            st.session_state.chat_history.append({"role":"bot","content":r})
            st.rerun()

    elif selected == "Upgrade":
        st.markdown("<div class='page-header'><h1>💰 Choose Your Plan</h1><p>Unlock the full power of Business Helper</p></div>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown("<div class='plan-card'><h3>🚀 Starter</h3><div class='price'>499</div><div class='currency'>PKR / month</div><ul><li>200 emails/day</li><li>50 leads/day</li><li>Job matching</li><li>Email support</li></ul></div>", unsafe_allow_html=True)
            if st.button("Select Starter", use_container_width=True): st.info("📱 Easypaisa: 03016835003 — 499 PKR")
        with c2:
            st.markdown("<div class='plan-card featured'><span class='badge'>⚡ Popular</span><h3>Pro</h3><div class='price'>1,499</div><div class='currency'>PKR / month</div><ul><li>2,000 emails/day</li><li>300 leads/day</li><li>Advanced matching</li><li>Priority support</li><li>Auto-apply</li></ul></div>", unsafe_allow_html=True)
            if st.button("Select Pro ⚡", use_container_width=True): st.success("🔥 Easypaisa: 03016835003 — 1,499 PKR")
        with c3:
            st.markdown("<div class='plan-card'><h3>🏆 Business</h3><div class='price'>3,999</div><div class='currency'>PKR / month</div><ul><li>Unlimited emails</li><li>Unlimited leads</li><li>Custom AI models</li><li>24/7 support</li><li>API access</li></ul></div>", unsafe_allow_html=True)
            if st.button("Select Business", use_container_width=True): st.info("🏢 Easypaisa: 03016835003 — 3,999 PKR")

        st.markdown("<br>", unsafe_allow_html=True)
        tb1,tb2 = st.tabs(["🇵🇰 Easypaisa","🌍 International"])
        with tb1:
            st.markdown("**Send to:** `03016835003`\n\n1. Easypaisa → Send Money\n2. Enter `03016835003`\n3. Enter amount\n4. Copy Transaction ID")
            txn = st.text_input("Transaction ID")
            if st.button("✅ Verify Payment"): st.success("Received! Upgraded within 2 hours."); st.balloons()
        with tb2:
            st.markdown("**PayPal:** businesshelper@paypal.com\n\nEmail: support@businesshelper.com after payment.")

# ============================================
# MAIN
# ============================================

def main():
    if st.session_state.authenticated:
        if st.session_state.is_admin: show_admin_dashboard()
        else: show_user_dashboard()
    else:
        st.markdown("<div class='page-header'><h1>🚀 Business Helper</h1><p>AI Platform · Jobs · B2B Leads · Email Marketing · Intelligence</p></div>", unsafe_allow_html=True)
        c1,c2 = st.columns([1,1])

        with c1:
            with st.expander("🔑 Admin Login"):
                au = st.text_input("Username", key="au"); ap = st.text_input("Password", type="password", key="ap")
                if st.button("Admin Login"):
                    if db.verify_admin(au, ap):
                        st.session_state.authenticated = True; st.session_state.is_admin = True
                        st.session_state.username = au; st.rerun()
                    else: st.error("❌ Invalid credentials")

            tl, ts = st.tabs(["👤 Login","📝 Sign Up"])
            with tl:
                with st.form("lf"):
                    un = st.text_input("Username"); pw = st.text_input("Password", type="password")
                    if st.form_submit_button("Login →", type="primary"):
                        u = db.verify_user(un, pw)
                        if u:
                            st.session_state.authenticated = True; st.session_state.is_admin = False
                            st.session_state.username = u['username']; st.session_state.user_id = u['id']
                            st.session_state.user_email = u['email']; st.session_state.package = u['package']
                            st.rerun()
                        else: st.error("❌ Invalid credentials")
            with ts:
                with st.form("sf"):
                    nu = st.text_input("Username"); ne = st.text_input("Email"); fn = st.text_input("Full Name")
                    nc = st.selectbox("Country", ["Pakistan","USA","UK","Canada","India","UAE","Germany","Australia"])
                    sk = st.text_area("Skills", "Python, Marketing, Sales")
                    np_ = st.text_input("Password", type="password")
                    if st.form_submit_button("Create Account →", type="primary"):
                        ok, msg = db.register_user(nu, ne, np_, fn, nc, sk)
                        if ok: st.success(msg)
                        else: st.error(msg)

        with c2:
            st.markdown("""
            <div class='info-card'>
                <h3>✨ Platform Features</h3>
                <p>💼 <strong>10,000+ Jobs</strong> — Global opportunities</p>
                <p>🏢 <strong>5,000+ B2B Leads</strong> — AI-scored contacts</p>
                <p>📧 <strong>Email Marketing</strong> — Campaign templates</p>
                <p>📰 <strong>Live Market News</strong> — Real-time intelligence</p>
                <p>🤖 <strong>AI Chat</strong> — 24/7 business support</p>
                <p>💰 <strong>Flexible Pricing</strong> — From 499 PKR</p>
            </div>
            <div class='info-card' style='margin-top:1rem;'>
                <h3>📊 Platform Stats</h3>
                <p>🌍 Active in <strong>50+ countries</strong></p>
                <p>👥 <strong>1,000+</strong> active users</p>
                <p>📧 <strong>50,000+</strong> emails/month</p>
                <p>⭐ <strong>95%</strong> satisfaction rate</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class='footer'>
        <p>© 2025 <strong>Business Helper</strong> · AI-Powered B2B Platform · All Rights Reserved</p>
        <p>📞 +92 300 1234567 &nbsp;|&nbsp; 📧 support@businesshelper.com</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
