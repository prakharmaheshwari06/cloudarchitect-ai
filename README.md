# ☁️ CloudArchitect AI - AWS Solution & Cost Advisor

An intelligent AWS Architecture Advisor designed for students, cloud practitioners, and hackathon builders.

## 🎯 Problem Statement
Students and new developers building prototypes often struggle to decide:
1. Which AWS services to pick (Compute, Storage, Database, Auth).
2. How to connect the services in a scalable request flow.
3. Whether their architecture fits inside the **AWS 12-Month Free Tier** or risks unexpected billing.

## 🚀 Key Features
- **Smart AWS Service Stack:** Maps requirements to appropriate services (Lambda, Rekognition, S3, DynamoDB, Cognito, API Gateway).
- **Interactive Request Flow Diagram:** Visual flowchart rendered with Mermaid.js.
- **AWS Free Tier Feasibility Audit:** Highlights zero-cost limits and potential cost pitfalls.
- **AWS Well-Architected Framework Checklist:** Security, reliability, and cost-optimization recommendations aligned with **AWS Cloud Practitioner (CLF-C02)** standards.

## 🛠️ Tech Stack
- **Frontend / Dashboard:** Streamlit (Python)
- **AI Engine:** Google Gemini (via REST API)
- **Diagrams:** Mermaid.js
- **Target Ecosystem:** Amazon Web Services (AWS)

## 🏃 Quick Start
```bash
# Install dependencies
pip install streamlit requests

# Launch the app
python -m streamlit run app.py
```
