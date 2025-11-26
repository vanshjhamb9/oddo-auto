# Odoo + Razorpay Integration Guide for Bodhih.com

## Overview
This guide explains how to integrate the webhook with your Odoo 18.4 SAAS. Since Odoo SAAS doesn't expose custom field mapping in the Razorpay configuration, we use a simple approach: **pass product details via the Description field**.

---

## How It Works

```
Odoo Sale Order
    ↓
    Add product name in Description
    ↓
Complete Razorpay Payment
    ↓
Razorpay sends description to webhook
    ↓
Webhook detects assessment type (DISC or Harrason)
    ↓
Routes to correct API & sends confirmation email
```

---

## Step 1: Configure Razorpay in Odoo

1. Go to **Accounting** → **Configuration** → **Payment Providers** → **Razorpay**
2. Click **Credentials** tab and verify your Account ID is set
3. That's it! No custom field mapping needed.

---

## Step 2: Create Sale Orders with Product Details

### For DISC Assessments:

When creating a sale order in Odoo:

1. **Select Product**: DISC Asia+ Basic Report (or any DISC product)
2. **Customer**: Add the customer details (name, email)
3. **Description Field**: Enter the assessment name

   Examples:
   ```
   DISC Asia+ Basic Report
   DISC Self-Awareness Advanced Report
   DISC Leadership Quick Assessment
   ```

4. **Confirm & Process Payment** through Razorpay

### For Harrason Assessments:

1. **Select Product**: Harrason Assessment (or any Harrason product)
2. **Customer**: Add the customer details
3. **Description Field**: Enter the assessment name

   Examples:
   ```
   Harrason Leadership Assessment
   Harrason Team Dynamics Assessment
   Harrason Executive Coaching Program
   ```

4. **Confirm & Process Payment** through Razorpay

---

## Step 3: What Happens Next

Once payment is confirmed through Razorpay:

1. **Webhook receives payment confirmation**
2. **Webhook extracts description** (product name)
3. **Webhook detects keywords**:
   - If description contains "disc" → Uses DISC Asia+ API
   - If description contains "harrason" → Uses Harrason API
4. **Webhook registers customer** on assessment platform
5. **Webhook sends email** with:
   - Login credentials
   - Assessment link
   - Payment confirmation

---

## Important: Product Naming

Make sure your **product names clearly indicate the assessment type**:

✅ GOOD:
- "DISC Asia+ Basic Report"
- "DISC Self-Awareness Advanced"
- "Harrason Leadership Assessment"
- "Harrason Team Building Program"

❌ AVOID:
- "Assessment 1" (no keywords)
- "Product A" (confusing)
- "Report" (too generic)

---

## Testing

### To Test the Integration:

1. Create a **test sale order** with:
   - Product: DISC Asia+ Basic Report
   - Customer: Your test email
   - Description: "DISC Asia+ Basic Report"

2. **Complete the payment** using Razorpay test mode

3. **Check webhook logs** in Replit to see:
   ```
   NEW PAYMENT FROM ODOO WEBSITE — BODHIH.COM
   Description: DISC Asia+ Basic Report
   Report Type: DISC Asia+ Basic
   Router to: DISC ASIA+
   ```

4. **Verify email sent** to your test email address

---

## Troubleshooting

### Email Not Received?
- Check email is correct in Odoo customer record
- Verify SMTP settings in Replit are correct
- Check spam/promotions folder in Gmail

### Wrong Assessment Type Detected?
- Check product name has "disc" or "harrason" keyword
- Make sure description field is filled in sale order
- Check webhook logs for the exact product name received

### Payment Not Processed?
- Verify Razorpay is enabled in Odoo
- Check payment status in Razorpay dashboard
- Verify webhook URL is set correctly in Razorpay

---

## Webhook URL

When setting up Razorpay webhooks (if needed), use:
```
https://your-replit-url.repl.co/razorpay-webhook
```

Event to listen for: `payment.captured`

---

## Support

For issues:
1. Check webhook logs in Replit project
2. Verify product names contain clear keywords
3. Ensure SMTP credentials are correct

Your webhook is production-ready! 🚀
