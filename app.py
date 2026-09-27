from flask import Flask, render_template, request, jsonify, Response, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')


#Configuration

projects_data = {
    "home-decor": {
        "title": "Home Decor Product (Sales Campaign)",
        "business_overview": """Type: Online Home Decor Store
Product: LED Wall Lamps
Goal: Increase Online Sales""",
        "problem": """Low Product Awareness
No Structure Ad funnel
Poor engagement on existing posts""",
        "strategy":"""<b>Funnel:</b>
Cold Audience > Product Video Ad
Retarget > View Content, Engagers, Add to Cart

<b>Core Idea:</b>
Sell <b>aesthetic transformation</b>, not just the product
'People don't buy lamps, they buy the vibe it creates in their home.'""",
        "audience": """<b>Cold Audience:</b>
Age: 20-36
Interests: Home Decor, Interior Design, Aesthetics, IKEA, home styling
<b>Warm Audience:</b>
Website Visitors (last 30 days)
Video Viewers with 50%+ watch-time
Instagram Engagers (last 30 days)""",
        "ad_copy": """<b>Headline:</b>
Transform Your Room Today!
<b>Primary Text:</b>
Tired of dull walls? Transform your room in seconds.
Modern LED wall lamps that instantly upgrade your space.

Limited  stock available - Order now and light up your life!""",
        "creative": """<b>Best format:</b>
Short video (7-15 seconds)
<b>Visual Concept:</b>
Before (Boring wall)
After (lamp ON, aesthetic lighting, cozy vibe)
Text overlay:
Before > After
Instant Room Upgrade """,
        "budget": """<b>Total Budget:</b>
10,000 PKR
<b>Split:</b>
Cold Traffic: 70%
Retargeting: 30%
<b>Optimization Goal:</b>
Conversions (Purchases)""",
        "results": """CTR: 2-4%
CPC: 15-30 PKR
Conversion Rate: 3-6%
ROAS: 2.5x-4x"""
    },
    "customer-churn": {
        "title": "Customer Churn Prediction",
        "Overview": "Created a Machine Learning model to predict Customer Churn.",
        "target": "Identify which cusotmers are going to leave or withdraw.",
        "approach": "Used Data Cleaning, Feature Engineering and Data Visualisation for EDA and trained ML Model using Logistic Regression.",
        "results": "Predicted Customer Churn with <b>82.5% Accuracy.</b>"
    },
    "gym-lead": {
        "title": "Gym Lead Generation Campaign",
        "business_overview": "Offered 1 Week Free Trial to attract members to a local Gym and increase Monthly Memberships.",
        "problem": "Gym has no consistent leads and they have no structured funnel.",
        "strategy": """Funnel: Cold audience > Lead form > WhatsApp follow-up.
Approach: Strong offer (free trial), Local trageting""",
        "audience": """Location: 5-8 km radius
Age: 18-40
Interests: Fitness, Health, weight loss, BodyBuilding""",
        "ad_copy": """<b>Headline:</b>
Start your Fitness Journey Today        

<b>Primary Text:</b>
Want to get fit but don't know where to start?
Try our gym FREE for 7 days.
No commitment, No pressure. Just results!
Limited slots available this week. Sign up now!""",
        "creative": """Gym Interior + people working out.
Text overlay: 7-Day Free Trial""",
        "budget": """Daily Budget: 1000 PKR.
Duration: 7 days.
Total: 6000 PKR.""",
        "results": """Cost per Lead: 80-140 PKR.
Total Leads: 60+ in one week.
Conversion to members: 7-10 new members."""
    },
    "ad-creative-analyzer": {
        "title": "Meta Ad Creative Analyzer",
        "overview": """<b>AI-Powered Ad Creative Analyzer</b> is a decision-support tool designed to help advertisers evaluate Meta ad creatives before launching them. It analyzes key creative elements, generates an overall score, and provides actionable suggestions to help determine whether a creative is ready for testing or needs refinement.""",
        "problem": """Advertisers and media buyers routinely burn budget testing creatives doomed to fail due to subjective guesswork. Without a systematic pre-launch audit framework, weak hooks, ambiguous messaging or cluttered visual hierarchies leak performance early, resulting in low CTRs and poor engagement.""",
        "approach": """<b>Diagnostic Scoring Rubric:</b> Structured a multi-point evaluation system grading visual stopping power, message congruence, value proposition clarity, and call-to-action strength.

<b>AI & Engineering Stack:</b> Leveraged multimodal AI models and Python workflows to parse image composition, text overlays, and primary ad copy against conversion-focused Meta ad benchmarks.

<b>Prescriptive Feedback Engine:</b> Programmed the system to generate prescriptive fixes alongside the numerical score, showing media buyers exactly which elements to tweak to reach launch viability.""",
        "results": """The result is a practical <b>AI-powered decision-support system</b> that gives advertisers a structured way to assess creatives before launch. Rather than replacing human judgment, it helps make the creative review process more consistent, data-informed, and actionable."""
    }
}

#This route generates the sitemap.xml. So Google bots can crawl for case studies and other pages.

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    base_url = "https://masahirabbas.online"
    # Static pages
    pages = [
        {"loc": f"{base_url}/", "changefreq": "weekly", "priority": "1.0"}
    ]
    # Dynamic Case Studies
    for project_id in projects_data.keys():
        pages.append({
            "loc": f"{base_url}/case-study/{project_id}",
            "changefreq": "monthly",
            "priority": "0.8"
        })

    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for p in pages:
        sitemap_xml.append('  <url>')
        sitemap_xml.append(f'    <loc>{p["loc"]}</loc>')
        sitemap_xml.append(f'    <changefreq>{p["changefreq"]}</changefreq>')
        sitemap_xml.append(f'    <priority>{p["priority"]}</priority>')
        sitemap_xml.append('  </url>')
    sitemap_xml.append('</urlset>')

    return Response("\n".join(sitemap_xml), mimetype='application/xml')

@app.route('/robots.txt', methods=['GET'])
def robots():
    content = "User-agent: *\nAllow: /\nSitemap: https://masahirabbas.online/sitemap.xml"
    return Response(content, mimetype='text/plain')

#Case Study Route
@app.route('/case-study/<project_id>', methods=['GET'])
def case_study(project_id):
    # Dictionary se project ka data uthayein
    project = projects_data.get(project_id)
    
    # Agar project URL theek hai toh page dikhayein, warna 404 Not Found
    if project:
        return render_template('case_study.html', project=project)
    return "Project Not Found", 404


#Receiving Email and its App Password 

MY_EMAIL = "masahirshah@gmail.com"
EMAIL_PASSWORD = None

# Logic to test for the text file first (Local Development)
try:
    with open("password.txt", "r") as file:
        # .strip() is crucial to remove any hidden newlines or spaces
        EMAIL_PASSWORD = file.read().strip()
except FileNotFoundError:
    # Counterpoint fallback: If the file doesn't exist (e.g., on Vercel), 
    # look for the environment variable instead.
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# Add a safety check so it doesn't crash silently later
if not EMAIL_PASSWORD:
    print("Email password could not be found!")
@app.route('/', methods=['GET'])
def home():
# connects with HTML from templates folder
    return render_template('index.html')


@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.json
    client_email = data.get('email')
    client_problem = data.get('message')

    # Basic Validation
    if not client_email or not client_problem:
        return jsonify({"status": "error", "message": "Email and problem description are required."}), 400

    # --- EMAIL ROUTING LOGIC ---
    try:
        msg = MIMEMultipart()
        msg['From'] = MY_EMAIL
        msg['To'] = MY_EMAIL # Sends email to my email inbox
        msg['Subject'] = f"New Lead: Strategy Consultation ({client_email})"

        # Email body structure
        body = f"A new prospect has reached out via your portfolio.\n\nProspect Email: {client_email}\n\nDetails: \n{client_problem}"
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(MY_EMAIL, EMAIL_PASSWORD)
        
        # Dispatch Email
        server.sendmail(MY_EMAIL, MY_EMAIL, msg.as_string())
        server.quit()

        print(f"Success: Lead routed to {MY_EMAIL}")
        return jsonify({"status": "success", "message": "Message Submitted Successfully!"}), 200

    except Exception as e:
        print(f"SMTP Error: {e}")
        # Passing the exact error 'e' to the frontend for debugging
        return jsonify({"status": "error", "message": f"Debug Error: {str(e)}"}), 500

def open_portfolio():
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")

open_portfolio()

if __name__ == '__main__':
    print("AI Portfolio Server is active...")

    app.run(debug=True, port=5000)