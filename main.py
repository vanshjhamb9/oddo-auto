# main.py → FINAL AUTOMATION FOR BODHIH.COM (LIVE & PERFECT)
# Razorpay Payment → Extract Type from Product → Register on DISC Asia+ → Send Email

from flask import Flask, request
import requests
from datetime import datetime
import logging
import os
import smtplib
from email.message import EmailMessage
import secrets
import string
import json
import re
import sys

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

DISC_API_URL       = os.environ.get("DISC_API_URL", "https://discapi.discasiaplus.org/api/DISC/Respondent_and_Report_Details_Bodhih")
DISC_CREDENTIAL    = os.environ.get("DISC_CREDENTIAL", "vezHgzd1EueI3clvF/1kNnMyCITD9UwC")

HARRASON_API_URL   = os.environ.get("HARRASON_API_URL", "")
HARRASON_CREDENTIAL = os.environ.get("HARRASON_CREDENTIAL", "")

SMTP_EMAIL         = os.environ.get("SMTP_EMAIL", "info@inowix.in")
SMTP_PASSWORD      = os.environ.get("SMTP_PASSWORD", "jxrmhihcvqlqojqa")
FROM_NAME          = os.environ.get("FROM_NAME", "Bodhi Training Solutions")
REPLY_TO_EMAIL     = os.environ.get("REPLY_TO_EMAIL", "support@bodhih.com")


def generate_password():
    return ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(12))


def extract_report_type(description):
    """Extract DISC type from product description - must match DISC API standards"""
    if not description:
        return "Basic"
    
    # Valid DISC types (check longer ones first to avoid partial matches)
    valid_types = [
        "Career entry level",
        "Team Build",
        "Communication",
        "Managerial",
        "Advanced",
        "Student",
        "Career",
        "Sales",
        "Basic",
        "Full"
    ]
    
    desc_lower = description.lower()
    for disc_type in valid_types:
        if disc_type.lower() in desc_lower:
            return disc_type
    
    return "Basic"

def register_on_disc_asia(name, display_name, email, gender, report_type):
    from datetime import timezone
    payload = {
        "credentials": {"encryptedPassword": DISC_CREDENTIAL},
        "respondentDetails": [{
            "name": name,
            "displayName": display_name,
            "gender": gender.title(),
            "eMailAddress": email,
            "type": report_type
        }],
        "transactionDetails": {
            "transactionId": 1,
            "transactionDate": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "isSuccessful": True
        }
    }

    try:
        logging.info(f"→ DISC API Call: {DISC_API_URL}")
        logging.info(f"→ Credential: {len(DISC_CREDENTIAL)} chars | {DISC_CREDENTIAL[:20]}...")
        logging.info(f"→ Request: Name={name}, Email={email}, Type={report_type}")
        
        r = requests.post(DISC_API_URL, json=payload, timeout=20)
        logging.info(f"→ Response Status: {r.status_code}")
        logging.info(f"→ Response Text: {r.text[:200]}")
        
        if r.status_code != 200:
            logging.info(f"✗ DISC HTTP ERROR {r.status_code}: {r.text[:300]}")
            return None
            
        result = r.json()
        if result.get("success") and result.get("respondentDetails"):
            link = result["respondentDetails"][0].get("link")
            logging.info(f"✓ DISC SUCCESS → Link: {link}")
            return link
        else:
            error = result.get('errorMessage', 'Unknown error')
            logging.info(f"✗ DISC FAILED → {error}")
            return None
    except Exception as e:
        logging.info(f"✗ DISC ERROR → {type(e).__name__}: {e}")
        return None

def register_on_harrason(name, display_name, email, gender, report_type):
    from datetime import timezone
    if not HARRASON_API_URL or not HARRASON_CREDENTIAL:
        logging.info("HARRASON API not configured - skipping")
        return None
    
    payload = {
        "credentials": {"encryptedPassword": HARRASON_CREDENTIAL},
        "respondentDetails": [{
            "name": name,
            "displayName": display_name,
            "gender": gender.title(),
            "eMailAddress": email,
            "type": report_type
        }],
        "transactionDetails": {
            "transactionId": 1,
            "transactionDate": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "isSuccessful": True
        }
    }

    try:
        r = requests.post(HARRASON_API_URL, json=payload, timeout=20)
        result = r.json()
        if result.get("success") and result.get("respondentDetails"):
            link = result["respondentDetails"][0].get("link")
            logging.info(f"HARRASON SUCCESS → {report_type} | Link: {link}")
            return link
        else:
            logging.info(f"HARRASON FAILED → {result.get('errorMessage')}")
            return None
    except Exception as e:
        logging.info(f"HARRASON EXCEPTION → {e}")
        return None

def send_email(name, email, amount, payment_id, report_type, assessment_link, password):
    msg = EmailMessage()
    msg['From'] = f"{FROM_NAME} <{SMTP_EMAIL}>"
    msg['To'] = email
    msg['Reply-To'] = REPLY_TO_EMAIL
    msg['Subject'] = f"Your {report_type} Assessment is Ready!"

    html = f"""
    <html>
    <body style="font-family:Arial,sans-serif;max-width:600px;margin:30px auto;padding:20px;background:#f9f9f9;border-radius:10px;">
        <h2 style="color:#2c3e50;text-align:center;">Payment Confirmed!</h2>
        <p>Dear <strong>{name}</strong>,</p>
        <p>Thank you for purchasing:</p>
        <h3 style="background:#e3f2fd;padding:15px;border-radius:8px;text-align:center;">
            {report_type} Assessment
        </h3>
        <p><strong>Amount Paid:</strong> ₹{amount:,.2f}<br><br>
           <strong>Payment ID:</strong> {payment_id}</p>

        <h3>Your Assessment Access</h3>
        <p><strong>Login Email:</strong> {email}<br><br>
           <strong>Password:</strong> <code style="background:#eee;padding:12px;font-size:15px;">{password}</code></p>

        <div style="text-align:center;margin:30px 0;">
            <a href="{assessment_link}" style="background:#1976d2;color:white;padding:16px 32px;text-decoration:none;border-radius:8px;font-size:18px;">
                Start Your Assessment Now
            </a>
        </div>

        <p style="background:#fff3cd;padding:15px;border-radius:8px;">
            This link is unique to you. Keep this email safe.
        </p>

        <p style="font-size:12px;color:#777;text-align:center;">
            Need help? Reply to this email.<br>
            Bodhi Training Solutions | www.bodhih.com
        </p>
    </body>
    </html>
    """
    msg.set_content("HTML email required.")
    msg.add_alternative(html, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(SMTP_EMAIL, SMTP_PASSWORD)
            s.send_message(msg)
        logging.info(f"EMAIL SENT → {email}")
    except Exception as e:
        logging.info(f"EMAIL FAILED → {e}")

def process_single_user(name, display_name, email, user_email, gender, product_name, product_type, report_type, amount, payment_id, description):
    """Process registration and email for a single user"""
    # Route to appropriate API based on product type
    assessment_link = None
    api_type = None
    
    if 'harrason' in product_type or 'harrason' in product_name.lower():
        api_type = "HARRASON"
        assessment_link = register_on_harrason(name, display_name, email, gender, report_type)
    elif 'disc' in product_type or 'disc' in product_name.lower() or not product_type:
        api_type = "DISC ASIA+"
        assessment_link = register_on_disc_asia(name, display_name, email, gender, report_type)
    else:
        logging.info(f"UNKNOWN PRODUCT TYPE: {product_type} - defaulting to DISC Asia+")
        api_type = "DISC ASIA+"
        assessment_link = register_on_disc_asia(name, display_name, email, gender, report_type)

    # Send email if registration succeeded
    if assessment_link:
        password = generate_password()
        send_email(name, user_email, amount, payment_id, report_type, assessment_link, password)
        logging.info(f"✓ {name}: {api_type} Account Created + Email Sent to {user_email}")
    else:
        logging.info(f"✗ {name}: {api_type} REGISTRATION FAILED — No email sent")

@app.route('/razorpay-webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True) or {}
    if not data or data.get('event') != 'payment.captured':
        return "ok", 200

    p = data['payload']['payment']['entity']
    notes = p.get('notes', {})
    description  = p.get('description', '')
    amount       = p['amount'] / 100
    order_id     = p.get('order_id', '')
    payment_method = p.get('method', '').upper()

    logging.info("\n" + "═" * 95)
    logging.info("NEW PAYMENT FROM ODOO WEBSITE — BODHIH.COM")
    logging.info("═" * 95)
    logging.info(f"Time           : {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    logging.info(f"Amount         : ₹{amount:,.2f}")
    logging.info(f"Payment ID     : {p['id']}")
    logging.info(f"Order ID       : {order_id}")
    logging.info(f"Phone          : {p.get('contact', '—')}")
    logging.info(f"Payment Method : {payment_method}")
    logging.info(f"Description    : {description}")
    
    # Log raw payload snippet for debugging
    raw_payload = json.dumps(data, indent=2)
    logging.info(f"Full Raw Payload (first 800 chars):")
    logging.info(raw_payload[:800])

    # Check if notes is a list (multiple users) or dict (single user)
    if isinstance(notes, list):
        # Multiple users - process each one
        logging.info(f"\n→ MULTIPLE USERS DETECTED: {len(notes)} users to register")
        for user_data in notes:
            if isinstance(user_data, dict):
                name = user_data.get('name', 'Customer')
                display_name = name
                email = user_data.get('email', p.get('email', 'no-email@bodhih.com'))
                user_email = user_data.get('user_email', email)
                gender = user_data.get('gender', 'Male')
                product_name = user_data.get('product_name', description)
                product_type = user_data.get('product_type', '').lower()
                report_type = extract_report_type(product_name or description)
                
                logging.info(f"\n→ Processing User: {name} ({user_email})")
                process_single_user(name, display_name, email, user_email, gender, product_name, product_type, report_type, amount, p['id'], description)
    else:
        # Single user - original logic
        name         = notes.get('name', p.get('contact', 'Customer'))
        display_name = name
        email        = p.get('email') or notes.get('user_email', 'no-email@bodhih.com')
        user_email   = notes.get('user_email', email)
        gender       = notes.get('gender', 'Male')
        product_id   = notes.get('product_id', '')
        product_name = notes.get('product_name', description)
        product_type = notes.get('product_type', '').lower()
        report_type = extract_report_type(product_name or description)

        logging.info(f"Customer Name  : {name}")
        logging.info(f"Email          : {email}")
        logging.info(f"Product ID     : {product_id or '—'}")
        logging.info(f"Product Name   : {product_name or '—'}")
        logging.info(f"Report Type    : {report_type}")
        
        process_single_user(name, display_name, email, user_email, gender, product_name, product_type, report_type, amount, p['id'], description)

    logging.info("═" * 95 + "\n")
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
