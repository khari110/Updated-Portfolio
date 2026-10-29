from flask import Flask, render_template, request, jsonify, Response, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')


#Configuration

projects_data = {
    "lead-generation-system": {
        "title": "Lead Generation System",
        "overview": """<b>Lead Generation System</b> is an AI automated solution designed to help marketing agencies discover potential clients and create personalized outreach emails. It streamlines the lead generation process by collecting prospect information and using AI to generate relevant email messages, reducing the manual effort required for client acquisition.""",
        "problem": """Marketing agencies often spend significant time searching for potential clients, gathering business information, and writing individual outreach emails. Manual prospecting can be repetitive, time-consuming, and difficult to scale.

Without an efficient lead generation workflow, agencies may struggle to maintain consistent outreach while focusing on their core marketing activities.""",
        "approach":"""<b>Automated Lead Collection:</b> Developed a workflow to identify and collect potential client leads from relevant sources, helping agencies streamline the prospecting process.

<b>Lead Data Processing:</b> Organized collected prospect information into a usable format, making it easier to review and prepare leads for outreach.

<b>Email Personalization:</b> Integrated AI to generate personalized cold emails based on available information about each prospect, making the outreach more relevant than generic email templates.

<b>End-to-End Workflow Automation:</b> Connected lead collection and email generation into a unified process to reduce repetitive manual tasks and make prospecting more efficient.'""",

        "results": """An <b>Automated Lead Generation System</b> that combines prospect collection with AI-powered email personalization in one workflow. It helps marketing agencies reduce manual prospecting effort, prepare personalized outreach more efficiently, and establish a more structured approach to client acquisition.

Rather than guaranteeing conversions, the system supports the outreach process by helping agencies spend less time on repetitive tasks and more time reviewing leads, building relationships, and developing business opportunities."""
    },
    "customer-churn": {
        "title": "Customer Churn Prediction",
        "Overview": "Created a Machine Learning model to predict Customer Churn.",
        "target": "Identify which cusotmers are going to leave or withdraw.",
        "approach": "Used Data Cleaning, Feature Engineering and Data Visualisation for EDA and trained ML Model using Logistic Regression.",
        "results": "Predicted Customer Churn with <b>82.5% Accuracy.</b>"
    },
    "social-media-posts- pipeline": {
        "title": "Social Media Posts Pipeline",
        "overview": "<b>Social Media Posts Pipeline</b> is an automation workflow designed to streamline social media content creation and publishing. The system aims to reduce repetitive manual work by connecting content research, post preparation, and publishing into a structured pipeline that helps maintain a consistent social media presence.",
        "problem": """Managing social media consistently requires more than writing captions. Businesses and marketing agencies must identify relevant topics, research audience interests, develop useful content, prepare posts, and publish them regularly.

Handling these tasks manually can be time-consuming for small teams and makes it difficult to maintain a consistent posting schedule. Repetitive content and generic posts can also reduce the relevance of social media content to the target audience.""",
        "approach": """<b>Workflow Automation:</b> Designed and developed an automation pipeline using n8n to connect social media content tasks into a structured workflow, reducing the need for repetitive manual operations.

<b>Content Research & Preparation:</b> Integrated AI in content research and preparation approach to identify relevant topics and audience problems, and supporting the preparation of social media posts, making the process more efficient and scalable.

<b>AI-Generated Visuals:</b> Incorporated AI image generation to create visuals aligned with the generated post content, connecting text and visual production within the same workflow.

<b>Email-Based Approval System:</b> Implemented an email approval step before publishing, allowing the content to be reviewed and approved or rejected by a human rather than automatically publishing every generated post.

<b>Google Sheets Content Tracking:</b> Integrated Google Sheets to record published topics, maintain a content history, and help prevent repetitive posts by tracking subjects that have already been covered.

<b>Structured Publishing Workflow:</b> Connected the different stages into a structured process that supports content preparation, human review, and publishing while reducing repetitive manual tasks.""",
        "results": """The result is an Automated Social Media Content Pipeline that provides a structured approach to researching, preparing, and managing social media posts. 

The system is designed to support the content production process rather than replace human judgment, allowing users to review content and maintain control over what gets published."""
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
    data = data = request.get_json() or {}
    if data.get('company'):
            return jsonify({'message': 'Message sent successfully!'}), 200
    client_email = data.get('email')
    client_problem = data.get('message')

    # Basic Validation
    if not client_email or not client_problem:
        return jsonify({"status": "error", "message": "Email and problem description are required."}), 400

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