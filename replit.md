# Razorpay Webhook Payment Automation for Bodhih.com

## Overview
This Flask-based webhook server automates the payment processing workflow for Bodhih Training Solutions. When a customer makes a payment through Razorpay (integrated with Odoo), the webhook:

1. Receives payment confirmation from Razorpay
2. Extracts product details from Razorpay notes field
3. Routes to the appropriate assessment API based on product type:
   - **DISC Asia+** for DISC assessments
   - **Harrason** for Harrason assessments
4. Registers the customer on the assessment platform
5. Sends a confirmation email with login credentials and assessment link

## Recent Changes (November 25, 2025)
- **Simplified Architecture**: Removed Odoo API dependency - now reads product details directly from Razorpay notes (passed by Odoo)
- **Configuration-Based Integration**: No code changes needed in Odoo - just configure Razorpay to pass product metadata
- **Harrason API Support**: Added support for Harrason assessment API alongside DISC Asia+
- **Enhanced Logging**: Comprehensive logging of payment data, product routing, and API responses
- **Security**: All credentials stored as encrypted secrets in Replit

## Project Architecture

### Main Components
- **main.py**: Flask webhook server
  - `/razorpay-webhook` (POST): Receives Razorpay `payment.captured` events
  
### API Integrations
1. **DISC Asia+ API**: For DISC personality assessments
2. **Harrason API**: For Harrason assessments (optional)
3. **Gmail SMTP**: For sending confirmation emails

### Product Routing Logic
The webhook determines which API to use based on product name:
- If product name contains **"disc"** (case-insensitive) → DISC Asia+
- If product name contains **"harrason"** (case-insensitive) → Harrason
- Default: DISC Asia+ (if no keywords match)

## Configuration

### Required Secrets
Set these in the Replit Secrets tab:
- `DISC_CREDENTIAL`: DISC Asia+ API credential
- `SMTP_EMAIL`: Gmail address for sending confirmation emails
- `SMTP_PASSWORD`: Gmail app password (NOT your regular password)

### Optional Secrets
- `HARRASON_API_URL`: Harrason API endpoint
- `HARRASON_CREDENTIAL`: Harrason API credential

### Optional Environment Variables
- `DISC_API_URL`: Override DISC API URL (defaults to production)
- `FROM_NAME`: Email sender name (default: "Bodhi Training Solutions")
- `REPLY_TO_EMAIL`: Reply-to email (default: support@bodhih.com)

## How to Set Up

### 1. Razorpay Webhook Configuration
Configure in Razorpay Dashboard:
```
Webhook URL: https://your-replit-url.repl.co/razorpay-webhook
Event: payment.captured
```

### 2. Odoo Configuration
In Odoo, configure Razorpay payment gateway to include product details in the notes field:

```json
{
    "product_id": "123",
    "product_name": "DISC Asia+ Basic Report",
    "product_type": "disc",
    "name": "Customer Name",
    "user_email": "customer@example.com",
    "gender": "Male"
}
```

**Key:** Product name should clearly indicate the assessment type:
- Use "DISC" or "disc" for DISC assessments
- Use "Harrason" or "harrason" for Harrason assessments

### 3. Set Replit Secrets
In Replit Secrets tab, add:
- `DISC_CREDENTIAL`: Your DISC Asia+ API key
- `SMTP_EMAIL`: Your Gmail address
- `SMTP_PASSWORD`: Your Gmail app password

### 4. Test the Integration
1. Create a test sale order in Odoo with a DISC product
2. Complete the Razorpay payment
3. Check webhook logs in Replit console
4. Verify confirmation email is sent to customer

## Testing
You can test the webhook locally by sending a POST request with a sample Razorpay payload:

```bash
curl -X POST http://localhost:5000/razorpay-webhook \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

## Deployment
This application is configured to run on Replit with autoscale deployment. The webhook server runs on port 5000 and is publicly accessible for receiving Razorpay webhooks.

## User Preferences
- Language: Python 3.11
- Framework: Flask (lightweight webhook server)
- Deployment: Replit (autoscale)
- Approach: Configuration-based (no code changes needed in Odoo)

## Files
- `main.py` - Flask webhook server
- `requirements.txt` - Python dependencies (Flask, requests)
- `ODOO_RAZORPAY_CONFIGURATION_GUIDE.md` - Odoo integration guide
- `test_webhook.py` - Local testing script
