"""
BUSINESS HELPER - COMPLETE PROFESSIONAL SYSTEM
Single File Application | Admin Controlled | Auto Email | Job Search | B2B Leads
Author: Business Helper Team
Version: 1.0.0
"""

# ============================================
# IMPORT ALL REQUIRED LIBRARIES
# ============================================

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

# ============================================
# API CREDENTIALS (YOUR PROVIDED KEYS)
# ============================================

ADZUNA_APP_ID = "71a53b73"
ADZUNA_API_KEY = "09e784ffc0f20280441bcef9bb73ad16"
NEWS_API_KEY = "03f7c2c09a7b45e1b25bc25bf4377fae"

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Business Helper - AI Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PROFESSIONAL CSS STYLING
# ============================================

st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Metric styling */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
    }
    
    /* Job card styling */
    .job-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Admin card styling */
    .admin-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
    }
    
    /* Chat styling */
    .chat-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
        text-align: right;
        float: right;
        clear: both;
    }
    
    .chat-bot {
        background: #f0f2f6;
        color: #1f2937;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
        text-align: left;
        float: left;
        clear: both;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        background: #1f2937;
        color: white;
        border-radius: 10px;
        margin-top: 50px;
    }
    
    /* Success badge */
    .success-badge {
        background: #4CAF50;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE MANAGEMENT CLASS
# ============================================

class DatabaseManager:
    """Complete database handler for Business Helper"""
    
    def __init__(self, db_path="business_helper.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                country TEXT,
                skills TEXT,
                package TEXT DEFAULT 'Free',
                created_date TEXT,
                last_login TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Admin table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                created_date TEXT
            )
        ''')
        
        # Jobs applied table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applied_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                job_title TEXT,
                company TEXT,
                applied_date TEXT,
                status TEXT
            )
        ''')
        
        # Leads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                industry TEXT,
                contact_person TEXT,
                email TEXT,
                phone TEXT,
                score REAL,
                status TEXT,
                created_date TEXT
            )
        ''')
        
        # Email campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_name TEXT,
                subject TEXT,
                body TEXT,
                recipient_count INTEGER,
                sent_date TEXT,
                status TEXT
            )
        ''')
        
        # Insert default admin if not exists
        cursor.execute("SELECT * FROM admin WHERE username = 'Hamad'")
        if not cursor.fetchone():
            hashed_password = hashlib.sha256("Hamad123@".encode()).hexdigest()
            cursor.execute('''
                INSERT INTO admin (username, password, email, created_date)
                VALUES (?, ?, ?, ?)
            ''', ("Hamad", hashed_password, "admin@businesshelper.com", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        conn.commit()
        conn.close()
    
    def verify_admin(self, username, password):
        """Verify admin credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, hashed_password))
        admin = cursor.fetchone()
        conn.close()
        return admin is not None
    
    def register_user(self, username, email, password, full_name, country, skills):
        """Register new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password, full_name, country, skills, package, created_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, hashed_password, full_name, country, skills, "Free", 
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "active"))
            conn.commit()
            return True, "Account created successfully!"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists!"
        finally:
            conn.close()
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT id, username, email, package, full_name, country FROM users WHERE username = ? AND password = ? AND status = 'active'", 
                      (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'package': user[3],
                'full_name': user[4],
                'country': user[5]
            }
        return None
    
    def get_all_users(self):
        """Get all registered users"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT id, username, email, full_name, country, package, created_date, status FROM users", conn)
        conn.close()
        return df
    
    def update_user_package(self, user_id, package):
        """Update user package"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET package = ? WHERE id = ?", (package, user_id))
        conn.commit()
        conn.close()
    
    def delete_user(self, user_id):
        """Delete user account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
    
    def get_system_stats(self):
        """Get overall system statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE package = 'Pro'")
        pro_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE package = 'Business'")
        business_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leads")
        total_leads = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM email_campaigns")
        total_campaigns = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM applied_jobs")
        total_applications = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total_users,
            'pro_users': pro_users,
            'business_users': business_users,
            'free_users': total_users - pro_users - business_users,
            'total_leads': total_leads,
            'total_campaigns': total_campaigns,
            'total_applications': total_applications
        }
    
    def add_lead(self, company_name, industry, contact_person, email, phone, score):
        """Add new business lead"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO leads (company_name, industry, contact_person, email, phone, score, status, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (company_name, industry, contact_person, email, phone, score, 'active', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    
    def get_all_leads(self):
        """Get all business leads"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM leads ORDER BY score DESC", conn)
        conn.close()
        return df
    
    def save_applied_job(self, user_id, job_title, company):
        """Save job application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO applied_jobs (user_id, job_title, company, applied_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, job_title, company, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'applied'))
        conn.commit()
        conn.close()
    
    def save_email_campaign(self, campaign_name, subject, body, recipient_count):
        """Save email campaign record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO email_campaigns (campaign_name, subject, body, recipient_count, sent_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (campaign_name, subject, body, recipient_count, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'sent'))
        conn.commit()
        conn.close()

# ============================================
# EMAIL AUTOMATOR CLASS
# ============================================

class EmailAutomator:
    """Professional email automation system"""
    
    def __init__(self):
        """Initialize email automator"""
        # Professional email templates
        self.templates = {
            "cold_outreach": """
Subject: Grow Your Business with AI Solutions - {company_name}

Dear {contact_name},

I hope this message finds you well. I'm reaching out because we've developed an AI-powered solution that can help {company_name} increase leads by 300% and automate customer outreach.

Our platform has helped 5,000+ businesses:
• Generate 10,000+ qualified leads monthly
• Automate email campaigns with 45% open rates
• Save 20+ hours weekly on manual tasks

Would you be open to a 15-minute demo this week?

Best regards,
Business Helper Team
+92 300 1234567
""",
            
            "follow_up": """
Subject: Following Up: AI Solutions for {company_name}

Hi {contact_name},

Just checking if you had a chance to review our AI business solutions for {company_name}.

We're currently offering a special 30% discount for early adopters, plus a free consultation worth $500.

Quick demo link: https://calendly.com/business-helper/demo

Looking forward to connecting!

Best,
Business Helper Team
""",
            
            "partnership": """
Subject: Strategic Partnership Opportunity - Business Helper × {company_name}

Dear {contact_name},

I see tremendous potential for a strategic partnership between Business Helper and {company_name}.

Our combined strengths could:
• Access 50,000+ businesses globally
• Share technology and resources
• Create integrated solutions for clients

Let's schedule a call to explore this opportunity.

Warm regards,
Business Helper Partnership Team
""",
            
            "newsletter": """
Subject: Weekly Business Insights + Special Offer for {company_name}

Hello {contact_name},

This week's top business trends:

📊 AI market grew 45% in Q1 2025
💼 Remote jobs increased 60% worldwide
🚀 Top 10 business automation tools

Special offer: Get 50% off on our Pro plan - Only this week!

Claim offer: bit.ly/business-helper-offer

Best,
Business Helper
"""
        }
    
    def generate_personalized_email(self, template_name, company_name, contact_name):
        """Generate personalized email using AI templates"""
        if template_name in self.templates:
            email_body = self.templates[template_name].format(
                company_name=company_name,
                contact_name=contact_name
            )
            return email_body
        return None

# ============================================
# API FUNCTIONS
# ============================================

def fetch_real_jobs(job_title, country):
    """Fetch real jobs from Adzuna API using your credentials"""
    country_codes = {
        "Pakistan": "pk", "USA": "us", "UK": "gb", "Canada": "ca",
        "India": "in", "UAE": "ae", "Germany": "de", "Australia": "au"
    }
    
    country_code = country_codes.get(country, "pk")
    
    url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "what": job_title,
        "results_per_page": 20,
        "content-type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for job in data.get('results', []):
                jobs.append({
                    'title': job.get('title', 'N/A'),
                    'company': job.get('company', {}).get('display_name', 'Unknown'),
                    'location': job.get('location', {}).get('display_name', 'Remote'),
                    'salary': f"{job.get('salary_min', 'N/A')} - {job.get('salary_max', 'N/A')}",
                    'description': job.get('description', '')[:300] + '...',
                    'url': job.get('redirect_url', '#')
                })
            return jobs
        else:
            return None
    except Exception as e:
        return None

def fetch_market_news():
    """Fetch real market news from News API"""
    url = f"https://newsapi.org/v2/top-headlines?category=business&apiKey={NEWS_API_KEY}&pageSize=10"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            news_items = []
            for article in data.get('articles', []):
                news_items.append({
                    'title': article.get('title', 'N/A'),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'url': article.get('url', '#'),
                    'published': article.get('publishedAt', '')
                })
            return news_items
        else:
            return None
    except:
        return None

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "package" not in st.session_state:
    st.session_state.package = "Free"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "applied_jobs" not in st.session_state:
    st.session_state.applied_jobs = []

# Initialize database
db = DatabaseManager()

# ============================================
# ADMIN DASHBOARD FUNCTIONS
# ============================================

def show_admin_dashboard():
    """Display admin control panel"""
    
    st.markdown("""
    <div class='header'>
        <h1>👑 Admin Control Panel</h1>
        <p>Complete System Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get system stats
    stats = db.get_system_stats()
    
    # Statistics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-container'>
            <h3>👥</h3>
            <h2>{stats['total_users']}</h2>
            <p>Total Users</p>
        </div>
        """, unsafe_all
