from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Purani line ko mita kar yeh likhen:
app = Flask(__name__, template_folder='templates', static_folder='static')

# --- CONFIGURATION ---

#Receiving Email and its App Password 
MY_EMAIL = "masahirshah@gmail.com"  
EMAIL_PASSWORD = "emtw klnr ncso cfzh"
@app.route('/', methods=['GET'])
def home():
    # Serves the index.html from the /templates folder
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
        msg['To'] = MY_EMAIL # Email aapko hi aayegi
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
    print("🚀 AI Portfolio Server is active (Direct-to-Inbox Mode)...")

    app.run(debug=True, port=5000)
