# main.py → RAZORPAY WEBHOOK WITH SO ID SCHEMA MAPPING
# Receives payment → Looks up SO in schema → Routes to DISC/Harrason → Sends email

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
DISC_CREDENTIAL    = os.environ.get("DISC_CREDENTIAL", "")

HARRASON_API_URL   = os.environ.get("HARRASON_API_URL", "")
HARRASON_CREDENTIAL = os.environ.get("HARRASON_CREDENTIAL", "")

SMTP_EMAIL         = os.environ.get("SMTP_EMAIL", "")
SMTP_PASSWORD      = os.environ.get("SMTP_PASSWORD", "")
FROM_NAME          = os.environ.get("FROM_NAME", "Bodhi Training Solutions")
REPLY_TO_EMAIL     = os.environ.get("REPLY_TO_EMAIL", "support@bodhih.com")

RAZORPAY_KEY_ID    = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")

# Load SO mapping schema
SO_MAPPING = {}
try:
    with open("so_mapping.json", "r") as f:
        data = json.load(f)
        SO_MAPPING = data.get("mappings", {})
        logging.info(f"✓ Loaded SO mapping schema with {len(SO_MAPPING)} entries")
except Exception as e:
    logging.info(f"⚠ Could not load SO mapping: {e}")


def get_assessment_from_so_mapping(so_number):
    """Look up assessment type and report type from SO ID mapping"""
    if so_number not in SO_MAPPING:
        logging.info(f"⚠ SO ID '{so_number}' not found in mapping - using defaults")
        return None
    
    mapping = SO_MAPPING[so_number]
    logging.info(f"✓ Found in SO mapping: {mapping.get('product_name')}")
    return mapping


def generate_password():
    return ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(12))


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
        logging.info(f"→ Request: Name={name}, Email={email}, Type={report_type}")
        
        response = requests.post(DISC_API_URL, json=payload, timeout=20)
        logging.info(f"→ Response Status: {response.status_code}")
        
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json.get("success"):
                respondent = resp_json.get("respondentDetails", [{}])[0]
                link = respondent.get("link", "N/A")
                logging.info(f"✓ DISC SUCCESS → Link: {link}")
                return {"success": True, "link": link, "respondent_id": respondent.get("respondentId")}
        
        logging.info(f"✗ DISC Error: {response.text[:300]}")
        return {"success": False}
        
    except Exception as e:
        logging.info(f"✗ DISC Exception: {type(e).__name__}: {str(e)[:100]}")
        return {"success": False}


def register_on_harrason(name, email, gender):
    """Register user on Harrason API"""
    if not HARRASON_API_URL or not HARRASON_CREDENTIAL:
        logging.info(f"✗ Harrason API not configured")
        return {"success": False}
    
    try:
        logging.info(f"→ Harrason API Call: {HARRASON_API_URL}")
        
        payload = {
            "name": name,
            "email": email,
            "gender": gender,
            "credential": HARRASON_CREDENTIAL
        }
        
        response = requests.post(HARRASON_API_URL, json=payload, timeout=20)
        logging.info(f"→ Response Status: {response.status_code}")
        
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json.get("success"):
                link = resp_json.get("link", "N/A")
                logging.info(f"✓ Harrason SUCCESS → Link: {link}")
                return {"success": True, "link": link}
        
        logging.info(f"✗ Harrason Error: {response.text[:300]}")
        return {"success": False}
        
    except Exception as e:
        logging.info(f"✗ Harrason Exception: {str(e)[:100]}")
        return {"success": False}


def send_confirmation_email(name, email, assessment_type, link, password):
    """Send confirmation email with assessment link"""
    try:
        if not SMTP_EMAIL or not SMTP_PASSWORD:
            logging.info(f"✗ Email credentials not configured")
            return False
        
        assessment_name = "DISC Assessment" if assessment_type == "disc" else "Harrason Assessment"
        
        msg = EmailMessage()
        msg["Subject"] = f"Your {assessment_name} Link - Bodhi Training Solutions"
        msg["From"] = f"{FROM_NAME} <{SMTP_EMAIL}>"
        msg["To"] = email
        msg["Reply-To"] = REPLY_TO_EMAIL
        
        body = f"""Hello {name},

Thank you for your purchase! Your {assessment_name} is ready.

Assessment Link: {link}

Your temporary password: {password}

Please change your password after first login.

Best regards,
{FROM_NAME}
support@bodhih.com
"""
        
        msg.set_content(body)
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)
        
        logging.info(f"✓ EMAIL SENT → {email}")
        return True
        
    except Exception as e:
        logging.info(f"✗ Email error: {str(e)[:100]}")
        return False


@app.route('/razorpay-webhook', methods=['POST'])
def razorpay_webhook():
    """Main webhook handler for Razorpay payment.captured events"""
    
    try:
        payload = request.json
        
        logging.info(f"═" * 100)
        logging.info(f"NEW PAYMENT FROM RAZORPAY WEBHOOK")
        logging.info(f"═" * 100)
        
        payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
        
        payment_id = payment_entity.get("id", "N/A")
        order_id = payment_entity.get("order_id", "")
        description = payment_entity.get("description", "")
        amount = payment_entity.get("amount", 0) / 100
        contact = payment_entity.get("contact", "N/A")
        email = payment_entity.get("email", "")
        method = payment_entity.get("method", "N/A")
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
        
        logging.info(f"Time           : {timestamp}")
        logging.info(f"Amount         : ₹{amount}")
        logging.info(f"Payment ID     : {payment_id}")
        logging.info(f"Order ID       : {order_id}")
        logging.info(f"Description    : {description}")
        logging.info(f"Phone          : {contact}")
        logging.info(f"Email          : {email}")
        logging.info(f"Payment Method : {method}")
        
        notes = payment_entity.get("notes", {})
        
        # Extract customer info
        customer_email = email
        customer_name = "Customer"
        
        if isinstance(notes, dict):
            customer_email = notes.get("customer_email") or notes.get("email") or email
            customer_name = notes.get("customer_name") or notes.get("name", "Customer")
        elif isinstance(notes, list) and notes:
            customer_email = notes[0].get("user_email") or notes[0].get("customer_email") or email
            customer_name = notes[0].get("name", "Customer")
        
        # Look up SO in mapping (primary method)
        assessment_mapping = get_assessment_from_so_mapping(description)
        
        if assessment_mapping:
            assessment_type = assessment_mapping.get("assessment_type", "disc")
            report_type = assessment_mapping.get("report_type", "Basic")
            product_name = assessment_mapping.get("product_name", "Unknown")
        else:
            # Fallback: determine from description if SO not in mapping
            assessment_type = "disc"
            report_type = "Basic"
            product_name = description
        
        logging.info(f"\nExtracted Data:")
        logging.info(f"  Product Name   : {product_name}")
        logging.info(f"  Customer Name  : {customer_name}")
        logging.info(f"  Customer Email : {customer_email}")
        logging.info(f"  Assessment Type: {assessment_type}")
        logging.info(f"  Report Type    : {report_type}")
        
        # Register based on type
        if assessment_type == "harrason":
            gender = "Male"  # Default
            result = register_on_harrason(customer_name, customer_email, gender)
        else:
            gender = "Male"  # Default
            result = register_on_disc_asia(customer_name, customer_name, customer_email, gender, report_type)
        
        # Send email if registration successful
        if result.get("success"):
            password = generate_password()
            send_confirmation_email(customer_name, customer_email, assessment_type, result.get("link", "N/A"), password)
        
        logging.info(f"═" * 100)
        return {"status": "ok"}, 200
        
    except Exception as e:
        logging.info(f"✗ WEBHOOK ERROR: {type(e).__name__}: {str(e)}")
        return {"status": "error"}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
