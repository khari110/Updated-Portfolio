from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


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
        "business_overview": "Created a Machine Learning model to predict Customer Churn.",
        "target": "Identify which cusotmers are going to leave or withdraw.",
        "approach": "Used Data Cleaning, Feature Engineering and Data Visualisation for EDA and trained ML Model using Logistic Regression.",
        "results": "Predicted Customer Churn with 82.5% accuracy"
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
    "ecommerce-sales": {
        "title": "Online Skincare Store (Sales Campaign)",
        "business_overview": """<b>Type:</b> Online Skincare Store.
<b>Product:</b> Acne Treatment Cream
<b>Goal:</b> Increase Online Sales""",
        "problem": """Low ROAS
No Retargeting strategy
Weak Product Awareness""",
        "strategy": """<b>Funnel:</b>
Cold Traffic > Product Page
Retarget > View Content
Retarget > Add to Cart""",
        "audience": """<b>Cold Audience:</b>
Age: 18-35
Interests: Skincare, Acne Treatment, Beauty Products

<b>Warm Audience:</b>
Website Visitors (last 30 days)
Instagram Engagers (last 30 days)""",
        "ad_copy": """<b>Headline:</b>
Clear Skin Starts Here!

<b>Primary Text:</b>
Struggling with acne that just don't go away?
Our dermatologist-tested formula helps reduce acne and improve skin clarity.

Try it Risk-free and See the Difference""",
        "creative": """Product close-up
Short demo (how to apply)""",
        "budget": """<b>Total Budget:</b>
20,000 PKR
<b>Split:</b>
Cold: 70%
Retarget: 30%""",
        "results": """CTR: 2-5%
CPC: 15-35 PKR
Conversion Rate: 3-7%
ROAS: 3x-4.5x"""
    }
}

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
EMAIL_PASSWORD = "emtw klnr ncso cfzh"
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
        body = f"A new prospect has reached out via your portfolio.\n\nProspect Email: {client_email}\n\nTheir Problem/Requirement:\n{client_problem}"
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
        return jsonify({"status": "error", "message": "Failed! Please try again later."}), 500

if __name__ == '__main__':
    print("AI Portfolio Server is active...")

    app.run(debug=True, port=5000)
