# Quick Start Guide - Razorpay Webhook for Bodhih.com

## ✅ System Status: READY

Your webhook server is up and running on Replit!

---

## 🚀 How to Use

### Step 1: Create Sale Orders in Odoo

When creating a sale order in Odoo 18.4:

1. Add the **assessment product** (DISC or Harrason)
2. In the **Description field**, write the product name clearly:
   
   **For DISC:**
   ```
   DISC Asia+ Basic Report
   DISC Self-Awareness Advanced Report
   DISC Leadership Assessment
   ```
   
   **For Harrason:**
   ```
   Harrason Leadership Assessment
   Harrason Team Dynamics Report
   ```

3. Fill in customer details (name, email)
4. Complete the Razorpay payment

### Step 2: Webhook Automatically:

✅ Receives payment from Razorpay
✅ Detects assessment type (DISC or Harrason)
✅ Registers customer on assessment platform
✅ Sends confirmation email with login credentials

---

## 📋 What's Configured

### Secrets (Encrypted in Replit):
- ✅ DISC_CREDENTIAL - DISC Asia+ API key
- ✅ SMTP_EMAIL - Your Gmail for sending emails
- ✅ SMTP_PASSWORD - Gmail app password

### Environment Variables:
- ✅ ODOO_URL = https://bodhih.odoo.com
- ✅ ODOO_DB = bodhih

### Webhook Endpoint:
```
https://your-replit-url.repl.co/razorpay-webhook
```

---

## 🔍 Troubleshooting

### Email Not Sending?
- Check that SMTP_EMAIL and SMTP_PASSWORD are correct
- Verify Gmail account has 2-factor enabled and app password is set

### Wrong Assessment Type?
- Make sure product name contains "disc" or "harrason"
- Check the description field in Odoo sale order

### Check Webhook Logs:
In Replit, go to **Logs** tab to see:
```
NEW PAYMENT FROM ODOO WEBSITE — BODHIH.COM
Product Name: DISC Asia+ Basic Report
Report Type: DISC Asia+ Basic
Router to: DISC ASIA+
```

---

## 📞 Support

If you encounter issues:
1. Check the webhook logs in Replit
2. Verify DISC credentials and email settings
3. Ensure product name contains "disc" or "harrason"

---

## 🎯 Next Steps

1. **Test with a real payment** through Razorpay
2. **Monitor the logs** to confirm everything works
3. **Verify email** is sent to customer with assessment link
4. **Deploy to production** when ready

Your system is ready! 🚀
