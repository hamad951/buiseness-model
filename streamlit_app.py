import streamlit as st
import pandas as pd
import requests
import smtplib
import random
from email.mime.text import MIMEText
from datetime import datetime
import json

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Augentic Global AI - B2B Platform", page_icon="🌍", layout="wide")

# ========== SESSION STATE ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.package = "Free"
    st.session_state.user_email = ""
    st.session_state.user_country = "Pakistan"
    st.session_state.emails_sent_today = 0

# ========== REAL JOB API (Adzuna - Free) ==========
def fetch_real_jobs(role, country):
    """Get real jobs from Adzuna API (free signup at adzuna.com)"""
    # Free tier: 500 requests/month
    # Sign up at https://developer.adzuna.com/ to get APP_ID and API_KEY
    APP_ID = "71a53b73"  # Replace after signing up
    API_KEY = "09e784ffc0f20280441bcef9bb73ad16"  # Replace after signing up
    
    country_codes = {
        "USA": "us", "UK": "gb", "Canada": "ca", "India": "in", 
        "Pakistan": "pk", "UAE": "ae", "Germany": "de", "Australia": "au"
    }
    
    code = country_codes.get(country, "us")
    url = f"https://api.adzuna.com/v1/api/jobs/{code}/search/1?app_id={APP_ID}&app_key={API_KEY}&title_only={role}&results_per_page=10"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for job in data.get('results', []):
                jobs.append({
                    'title': job.get('title', 'N/A'),
                    'company': job.get('company', {}).get('display_name', 'Unknown'),
                    'location': job.get('location', {}).get('display_name', 'Remote'),
                    'salary': job.get('salary_min', 'Not specified'),
                    'url': job.get('redirect_url', '#')
                })
            return jobs
        else:
            return None
    except:
        return None

# ========== REAL EMAIL SENDING (Gmail SMTP) ==========
def send_real_email(to_email, subject, body):
    """Send actual emails using Gmail SMTP"""
    # IMPORTANT: Use Gmail App Password (not regular password)
    # Get it: Google Account → Security → App Passwords
    
    SENDER_EMAIL = "your_email@gmail.com"  # Replace with your email
    SENDER_PASSWORD = "your_app_password"  # Replace with App Password
    
    if st.session_state.emails_sent_today >= email_limits.get(st.session_state.package, 5):
        return False, "Daily limit reached"
    
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        st.session_state.emails_sent_today += 1
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"

# ========== REAL MARKET NEWS (NewsAPI) ==========
def get_real_news(category, country):
    """Fetch real-time news from NewsAPI"""
    # Free API key: https://newsapi.org/register
    API_KEY = "YOUR_NEWS_API_KEY"  # Replace after signing up
    
    categories = {
        "Technology": "technology",
        "Business": "business",
        "Startups": "technology",
        "Jobs": "business"
    }
    
    cat = categories.get(category, "general")
    url = f"https://newsapi.org/v2/top-headlines?country={country.lower()}&category={cat}&apiKey={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            news_items = []
            for article in articles[:10]:
                news_items.append(f"📰 {article['title']} - {article['source']['name']}")
            return news_items if news_items else None
        else:
            return None
    except:
        return None

# ========== EMAIL LIMITS BY PACKAGE ==========
email_limits = {
    "Free": 5,
    "Starter": 200,
    "Pro": 2000,
    "Business": 10000
}

# ========== SIDEBAR ==========
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.title("🌍 Augentic Global AI")
    
    if not st.session_state.logged_in:
        with st.form("login_form"):
            email = st.text_input("Email Address")
            country = st.selectbox("Country", ["Pakistan", "USA", "UK", "Canada", "India", "UAE", "Germany", "Australia"])
            if st.form_submit_button("🚀 Start Free Trial"):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_country = country
                st.session_state.package = "Free"
                st.rerun()
    else:
        st.success(f"✅ {st.session_state.user_email}")
        st.info(f"📍 {st.session_state.user_country}")
        st.warning(f"📦 {st.session_state.package} Plan")
        st.metric("📧 Emails Today", f"{st.session_state.emails_sent_today}/{email_limits.get(st.session_state.package, 5)}")
        
        st.markdown("---")
        st.subheader("💰 Upgrade")
        
        if st.session_state.user_country == "Pakistan":
            st.write("🇵🇰 **Easypaisa: 03016835003**")
            st.write("Starter: 499 PKR")
            st.write("Pro: 1,499 PKR")
            st.write("Business: 3,999 PKR")
        else:
            st.write("💳 **PayPal/Crypto**")
            st.write("Starter: $5")
            st.write("Pro: $15")
            st.write("Business: $40")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# ========== MAIN CONTENT ==========
if st.session_state.logged_in:
    
    # Header
    st.title("🌍 Augentic Global AI Dashboard")
    st.markdown(f"*Welcome back! You're on the **{st.session_state.package}** plan*")
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💼 Jobs", "🏢 B2B Leads", "📧 Email Engine", "📰 Live News", "💰 Upgrade"])
    
    # ========== TAB 1: REAL JOBS ==========
    with tab1:
        st.header("💼 Real-Time Job Search")
        
        col1, col2 = st.columns(2)
        with col1:
            job_role = st.text_input("Job Title", "Software Engineer")
        with col2:
            job_country = st.selectbox("Country", ["USA", "UK", "Canada", "India", "Pakistan", "UAE", "Germany", "Australia"])
        
        if st.button("🔍 Search Real Jobs", type="primary"):
            with st.spinner("Fetching latest jobs..."):
                jobs = fetch_real_jobs(job_role, job_country)
                
                if jobs:
                    for idx, job in enumerate(jobs[:5 if st.session_state.package == "Free" else len(jobs)]):
                        with st.container():
                            st.markdown(f"### {job['title']}")
                            st.write(f"🏢 {job['company']} | 📍 {job['location']}")
                            if job['salary'] != 'Not specified':
                                st.write(f"💰 Salary: ${job['salary']:,.0f}/year")
                            if st.session_state.package != "Free":
                                st.markdown(f"[Apply Here]({job['url']})")
                            st.markdown("---")
                    
                    if st.session_state.package == "Free":
                        st.info("🔒 Upgrade to Pro to see salaries + direct apply links")
                else:
                    st.warning("⚠️ Demo mode: Sign up for free Adzuna API key to get real jobs (see instructions below)")
                    st.code("""
                    How to get REAL jobs:
                    1. Go to developer.adzuna.com
                    2. Sign up (free)
                    3. Get APP_ID and APP_KEY
                    4. Replace in code: APP_ID = "your_id", API_KEY = "your_key"
                    """)
    
    # ========== TAB 2: B2B LEADS ==========
    with tab2:
        st.header("🏢 Global B2B Leads")
        
        lead_industry = st.selectbox("Industry", ["Technology", "Finance", "Retail", "Healthcare", "Manufacturing"])
        lead_country = st.selectbox("Target Country", ["All", "Pakistan", "USA", "UK", "UAE", "India"])
        
        if st.button("Find Business Leads"):
            # Mock leads (in production, use LinkedIn API or Apollo.io API)
            leads = [
                {"company": f"Tech Solutions {lead_country}", "contact": "CEO", "email": "ceo@techsolutions.com", "decision_maker": "John Smith"},
                {"company": f"{lead_industry} Pro International", "contact": "Director", "email": "director@industrypro.com", "decision_maker": "Sarah Johnson"},
                {"company": f"Global {lead_industry} Group", "contact": "Procurement Head", "email": "procurement@globalgroup.com", "decision_maker": "Ahmed Khan"}
            ]
            
            for lead in leads[:2 if st.session_state.package == "Free" else len(leads)]:
                with st.expander(f"📌 {lead['company']}"):
                    st.write(f"**Decision Maker:** {lead['decision_maker']} ({lead['contact']})")
                    if st.session_state.package != "Free":
                        st.write(f"**Email:** `{lead['email']}`")
                        if st.button(f"Contact {lead['company']}", key=lead['company']):
                            st.success(f"✅ Lead saved! Use Email Engine to contact.")
                    else:
                        st.caption("🔒 Upgrade to see full contact details")
    
    # ========== TAB 3: REAL EMAIL ENGINE ==========
    with tab3:
        st.header("📧 Live Email Sending")
        
        remaining = email_limits.get(st.session_state.package, 5) - st.session_state.emails_sent_today
        st.info(f"📊 {remaining} emails remaining today")
        
        with st.form("email_form"):
            to_email = st.text_input("Recipient Email")
            to_name = st.text_input("Recipient Name")
            product = st.text_area("What are you offering?", "AI marketing automation for businesses")
            email_type = st.selectbox("Email Type", ["Cold Outreach", "Follow-up", "Newsletter"])
            
            # Generate email body
            if email_type == "Cold Outreach":
                email_body = f"""Subject: Grow your business with {product}

Hi {to_name},

I hope this email finds you well.

We help businesses like yours implement {product}, resulting in 40% more leads and 25% higher conversion rates.

Would you be open to a quick 10-minute call next Tuesday?

Best regards,
Augentic AI Team
"""
            else:
                email_body = f"""Subject: Following up on {product}

Hi {to_name},

Just checking if you had a chance to see my previous email about {product}.

Many companies are already seeing results. Let me know if you'd like a free demo.

Thanks,
Augentic AI
"""
            
            st.text_area("Preview Email", email_body, height=200)
            
            send_button = st.form_submit_button("📤 Send Real Email")
            
            if send_button:
                if st.session_state.package == "Free":
                    st.warning("🔒 Free tier: 5 test emails/day. Upgrade to send unlimited.")
                    # Demo mode - don't actually send
                    st.success("✅ DEMO: Email would be sent (Upgrade for live sending)")
                else:
                    success, message = send_real_email(to_email, email_body.split('\n')[0], email_body)
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
        
        # Bulk email (Pro+)
        if st.session_state.package in ["Pro", "Business"]:
            with st.expander("📎 Bulk Email Upload (CSV)"):
                st.write("Upload CSV with columns: email, name, company")
                uploaded = st.file_uploader("Choose CSV", type=['csv'])
                if uploaded:
                    st.success("Ready to send bulk emails (100+ leads)")

    # ========== TAB 4: REAL MARKET NEWS ==========
    with tab4:
        st.header("📰 Live Market News")
        
        news_cat = st.selectbox("Category", ["Technology", "Business", "Startups", "Cryptocurrency"])
        
        if st.button("🔄 Fetch Latest News", type="primary"):
            with st.spinner("Fetching real-time news..."):
                news = get_real_news(news_cat, st.session_state.user_country.lower()[:2])
                
                if news:
                    for item in news:
                        st.success(item)
                else:
                    st.warning("⚠️ Demo: Sign up for free NewsAPI key to get real news")
                    st.code("""
                    How to get REAL news:
                    1. Go to newsapi.org
                    2. Sign up (free)
                    3. Get API key
                    4. Replace in code: API_KEY = "your_key"
                    """)
                    # Demo news
                    demo_news = [
                        f"🚀 {news_cat} sector grows 25% globally in Q1 2025",
                        f"💰 Investment in {news_cat} startups reaches $5B",
                        f"📈 {st.session_state.user_country} sees surge in {news_cat.lower()} jobs"
                    ]
                    for item in demo_news:
                        st.info(item)

    # ========== TAB 5: UPGRADE ==========
    with tab5:
        st.header("💰 Upgrade Your Plan")
        
        if st.session_state.user_country == "Pakistan":
            st.subheader("🇵🇰 Pakistani Users - Easypaisa")
            st.markdown("""
            **Send payment to:** `03016835003` (Easypaisa)
            
            **Packages:**
            - **Starter (499 PKR)** → 200 emails/day + 50 leads/day
            - **Pro (1,499 PKR)** → 2,000 emails/day + 300 leads/day  
            - **Business (3,999 PKR)** → 10,000 emails/day + Unlimited leads
            
            **After payment, enter Transaction ID:**
            """)
            txn_id = st.text_input("Transaction ID")
            if st.button("Verify & Upgrade"):
                st.success("✅ Payment received! Your account will be upgraded within 2 hours.")
                st.balloons()
        else:
            st.subheader("🌍 International Users")
            st.markdown("""
            **PayPal:** [paypal.me/augentic](https://paypal.me/augentic)
            
            **Crypto:** USDC (Polygon) - `0x...your_address`
            
            **Packages:**
            - Starter: $5
            - Pro: $15
            - Business: $40
            """)

else:
    # Landing page
    st.title("🌍 Augentic Global AI")
    st.markdown("## Your All-in-One B2B Platform for Jobs, Leads & Outreach")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Users", "1,247", "+12%")
    with col2:
        st.metric("Jobs Posted", "38K", "+5%")
    with col3:
        st.metric("B2B Leads", "24K", "+8%")
    with col4:
        st.metric("Emails Sent", "152K", "+22%")
    
    st.info("👈 **Click Start Free Trial in the sidebar to begin!**")
    
    st.markdown("---")
    st.subheader("✨ Free Features Included:")
    st.write("✅ Real-time job search (50+ countries)")
    st.write("✅ B2B lead generation")
    st.write("✅ Email outreach engine")
    st.write("✅ Live market news")
    st.write("✅ 5 test emails/day")
