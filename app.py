import streamlit as st
import json
import os
import requests

# Set page layout and AWS-inspired styling
st.set_page_config(
    page_title="CloudArchitect AI - AWS Solution Advisor",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for AWS Branding
st.markdown("""
<style>
    .aws-header {
        background: linear-gradient(135deg, #1A222D 0%, #232F3E 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        border-left: 6px solid #FF9900;
    }
    .aws-badge {
        background-color: #FF9900;
        color: #111;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .service-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .free-tier-tag {
        color: #166534;
        background-color: #dcfce7;
        padding: 2px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Pre-baked Demo Data (Guarantees zero-fail demo if user has no API key)
DEMO_DATA = {
    "title": "LPU Campus Attendance & Facial Recognition System",
    "overview": "A scalable, serverless AWS architecture designed to process student attendance via camera feeds or mobile snapshots, matching faces against student records with high availability and minimal cost.",
    "services": [
        {"category": "Compute", "name": "AWS Lambda", "role": "Runs serverless microservices for image processing & API responses without running servers.", "free_tier": "1 Million requests/month free forever"},
        {"category": "AI / Vision", "name": "Amazon Rekognition", "role": "Analyzes student photos, extracts face landmarks, and matches against student facial embeddings.", "free_tier": "5,000 images/month free for 12 months"},
        {"category": "Storage", "name": "Amazon S3", "role": "Secure bucket storing encrypted student profile photos and attendance logs.", "free_tier": "5 GB standard storage free for 12 months"},
        {"category": "Database", "name": "Amazon DynamoDB", "role": "Ultra-fast NoSQL database tracking student check-ins, timestamps, and lecture roll numbers.", "free_tier": "25 GB storage & 200M requests/month free forever"},
        {"category": "Networking", "name": "Amazon API Gateway", "role": "Exposes secure REST endpoints for mobile app and classroom scanners.", "free_tier": "1 Million API calls/month free for 12 months"},
        {"category": "Auth & Security", "name": "Amazon Cognito", "role": "Handles student and faculty login with JWT tokens and Role-Based Access Control (RBAC).", "free_tier": "50,000 Monthly Active Users (MAUs) free forever"},
        {"category": "Monitoring", "name": "Amazon CloudWatch", "role": "Collects logs, traces Lambda execution, and triggers alarms on error spikes.", "free_tier": "10 custom metrics & 5 GB log ingestion free forever"}
    ],
    "mermaid": """graph TD
    Client["📱 Student / Faculty Mobile App"] -->|HTTPS / JWT| APIGW["🌐 Amazon API Gateway"]
    APIGW -->|Trigger| Lambda["⚡ AWS Lambda (Processing)"]
    Lambda -->|Upload Photo| S3["🪣 Amazon S3 (Image Storage)"]
    Lambda -->|Compare Face| Rekog["👁️ Amazon Rekognition"]
    Lambda -->|Save Record| DDB["💾 Amazon DynamoDB (Attendance Logs)"]
    Client -->|User Auth| Cog["🔐 Amazon Cognito"]
    Lambda -->|Telemetry| CW["📈 Amazon CloudWatch"]
    style Client fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
    style APIGW fill:#ffedd5,stroke:#ea580c,stroke-width:2px
    style Lambda fill:#fef3c7,stroke:#d97706,stroke-width:2px
    style S3 fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    style Rekog fill:#ede9fe,stroke:#7c3aed,stroke-width:2px
    style DDB fill:#fee2e2,stroke:#dc2626,stroke-width:2px
    style Cog fill:#f1f5f9,stroke:#475569,stroke-width:2px""",
    "cost_analysis": [
        "✅ **Zero Server Idle Cost:** Completely serverless. When no lectures are occurring, cost drops to ₹0.",
        "✅ **AWS Free Tier Coverage:** Lambda, DynamoDB, Cognito, and S3 are all comfortably inside the 12-month Free Tier for university testing.",
        "⚠️ **Watch-out Area:** Amazon Rekognition charges per image analyzed beyond the 5,000 free monthly tier."
    ],
    "well_architected": [
        "🔒 **Security:** S3 bucket configured with 'Block Public Access' and KMS AES-256 encryption.",
        "⚡ **Performance:** DynamoDB configured with Single-Table design using StudentID as partition key (PK) for single-digit millisecond queries.",
        "🛡️ **Cost Optimization:** Set up an AWS CloudWatch Billing Alert at $5 to prevent unexpected charges."
    ]
}

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Architecture Config")
    api_key = st.text_input("Gemini API Key (Optional)", type="password", help="Get a free key in 30 seconds at aistudio.google.com. Leave empty to run Demo Mode!")
    
    st.markdown("---")
    st.markdown("### 💡 Quick Campus Presets")
    preset = st.radio(
        "Choose an example:",
        [
            "Custom App Idea (Type your own)",
            "LPU Student Attendance & Face Recognition",
            "Campus Hostel Midnight Food Delivery",
            "College Notes & Past Exam Papers Portal",
            "Real-time AI Doubt Solver for Classrooms"
        ],
        index=1
    )

    st.markdown("---")
    st.markdown("""
    **Cloud Practitioner Tips:**
    - 🏷️ Serverless = Pay only for execution
    - 🛡️ Free Tier covers 12 months on new accounts
    - 🎯 Perfect for AWS CLF-C02 demonstrations
    """)

# Main Screen Header
st.markdown("""
<div class="aws-header">
    <span class="aws-badge">AWS CLOUD PRACTITIONER ASSISTANT</span>
    <h1 style="margin: 8px 0 4px 0; font-size: 2.2rem;">☁️ CloudArchitect AI</h1>
    <p style="margin: 0; opacity: 0.85; font-size: 1.05rem;">
        Describe any app idea — get an enterprise-grade AWS Service Stack, Live Flowchart, and Free-Tier Cost Audit.
    </p>
</div>
""", unsafe_allow_html=True)

# Form Inputs
col1, col2 = st.columns([3, 1])

preset_descriptions = {
    "LPU Student Attendance & Face Recognition": "A campus mobile app for students and faculty where attendance is marked via selfie facial recognition, storing logs securely and preventing proxy attendance.",
    "Campus Hostel Midnight Food Delivery": "A campus food ordering app for hostelers to order midnight snacks from local vendors, supporting real-time order tracking, Razorpay integration, and SMS alerts.",
    "College Notes & Past Exam Papers Portal": "A high-speed document sharing portal where university students upload and download lecture PDFs, search syllabus by course code, and view past 5 years question papers.",
    "Real-time AI Doubt Solver for Classrooms": "A real-time student Q&A assistant where students can post code snippets or exam doubts during lectures and receive instant AI solutions with faculty moderation."
}

default_text = preset_descriptions.get(preset, "")

with col1:
    user_prompt = st.text_area(
        "Describe your app or system requirements:",
        value=default_text if preset != "Custom App Idea (Type your own)" else "",
        placeholder="e.g. A ride-sharing app for campus students with live geolocation and push notifications...",
        height=110
    )

with col2:
    traffic = st.selectbox(
        "Expected Daily Users:",
        ["100 - 500 (Prototype)", "1,000 - 5,000 (Campus-wide)", "50,000+ (Scale)"],
        index=1
    )
    generate_btn = st.button("🚀 Design Architecture", type="primary", use_container_width=True)

# Function to call Gemini via REST API (No complex SDK dependency)
def query_gemini_api(prompt_text, traffic_level, key):
    system_instruction = f"""
    You are an expert AWS Principal Solutions Architect and AWS Cloud Practitioner trainer.
    Analyze the following project idea: "{prompt_text}". Daily users: {traffic_level}.
    
    You must output strictly valid JSON in the exact structure below, with no markdown fences, no formatting backticks:
    {{
        "title": "Short descriptive architecture title",
        "overview": "2-sentence high level architecture summary",
        "services": [
            {{
                "category": "Compute / Database / Storage / Networking / Security / AI / Monitoring",
                "name": "AWS Service Name (e.g. AWS Lambda)",
                "role": "Concise description of why this service is chosen and what it handles",
                "free_tier": "Exact AWS Free Tier allowance for this service"
            }}
        ],
        "mermaid": "graph TD\\nClient[📱 Mobile / Web App] -->|HTTPS| APIGW[🌐 Amazon API Gateway]\\nAPIGW --> Lambda[⚡ AWS Lambda]\\nLambda --> DDB[(💾 Amazon DynamoDB)]",
        "cost_analysis": [
            "Bullet point 1 on free tier fit",
            "Bullet point 2 on cost saving / serverless benefits",
            "Bullet point 3 on any watch-out areas"
        ],
        "well_architected": [
            "Security pillar best practice",
            "Reliability / Performance pillar practice",
            "Cost optimization pillar practice"
        ]
    }}
    Ensure the mermaid graph is clean and valid.
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": system_instruction}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    res = requests.post(url, json=payload, timeout=25)
    if res.status_code == 200:
        data = res.json()
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(raw_text)
    else:
        raise Exception(f"API Error {res.status_code}: {res.text}")

# Main Logic
architecture_data = None

if generate_btn:
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a project description or select a preset!")
    elif api_key:
        with st.spinner("Designing AWS Solution Architecture with Gemini AI..."):
            try:
                architecture_data = query_gemini_api(user_prompt, traffic, api_key)
                st.success("✅ Custom Architecture Generated Live!")
            except Exception as e:
                st.error(f"Error connecting to AI: {str(e)}. Showing pre-computed architecture instead.")
                architecture_data = DEMO_DATA
    else:
        # Seamless Instant Demo Mode (No API key required)
        st.info("💡 Running in Instant Demo Mode (Enter a free Gemini API key in sidebar for live custom prompts).")
        architecture_data = DEMO_DATA
elif preset != "Custom App Idea (Type your own)":
    # Show demo data by default on first load so screen is never empty!
    architecture_data = DEMO_DATA

# Display Architecture Results
if architecture_data:
    st.markdown("---")
    st.markdown(f"### 📋 {architecture_data.get('title', 'AWS Architecture Solution')}")
    st.markdown(f"> *{architecture_data.get('overview', '')}*")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏗️ AWS Service Stack", 
        "📊 Architecture Diagram", 
        "💰 Free-Tier & Cost Audit", 
        "🛡️ Well-Architected Checklist"
    ])

    with tab1:
        st.markdown("#### Selected AWS Services & Justification")
        cols = st.columns(2)
        services = architecture_data.get("services", [])
        for idx, svc in enumerate(services):
            target_col = cols[idx % 2]
            with target_col:
                st.markdown(f"""
                <div class="service-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <span style="font-weight:700; font-size:1.05rem; color:#0f172a;">{svc.get('name')}</span>
                        <span class="free-tier-tag">Free Tier</span>
                    </div>
                    <p style="margin:0 0 6px 0; font-size:0.85rem; color:#475569;"><b>Category:</b> {svc.get('category')}</p>
                    <p style="margin:0 0 8px 0; font-size:0.9rem; color:#1e293b;">{svc.get('role')}</p>
                    <div style="font-size:0.8rem; color:#059669; font-weight:500;">
                        🎁 <i>{svc.get('free_tier')}</i>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("#### Cloud Request Flow (Mermaid Diagram)")
        mermaid_code = architecture_data.get("mermaid", "")
        if mermaid_code:
            st.markdown(f"```mermaid\n{mermaid_code}\n```")
        st.info("💡 **Flow Breakdown:** Client requests hit CloudFront/API Gateway, invoke stateless Lambda functions, and read/write to managed DynamoDB/S3 with full telemetry logged in CloudWatch.")

    with tab3:
        st.markdown("#### 💵 AWS Billing & Free-Tier Feasibility")
        for pt in architecture_data.get("cost_analysis", []):
            st.markdown(f"- {pt}")
        
        st.markdown("---")
        st.markdown("""
        **🎓 Cloud Practitioner Exam Concept Highlight:**
        - **AWS Cost Explorer:** Used to forecast and track cloud spending over time.
        - **AWS Budgets:** Set custom spending thresholds and send email/SMS alerts before charges occur.
        - **Always Free Services:** DynamoDB (25 GB), Lambda (1M requests/mo), CloudWatch (10 metrics).
        """)

    with tab4:
        st.markdown("#### 🛡️ AWS Well-Architected Framework Alignment")
        for pillar in architecture_data.get("well_architected", []):
            st.markdown(f"- {pillar}")
        
        st.markdown("---")
        st.markdown("""
        **Cloud Practitioner Rule of Thumb:**
        - Never use Root AWS Account for day-to-day operations. Always create an IAM user with MFA.
        - Enable S3 Default Encryption (SSE-S3 or KMS) on all buckets.
        """)
