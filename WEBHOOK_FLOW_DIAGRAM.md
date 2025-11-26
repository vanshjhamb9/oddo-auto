# Webhook Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CUSTOMER PURCHASES                           │
│                     (on Bodhih Odoo Website)                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ODOO PAYMENT FLOW                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ Sale Order Created                                          │    │
│  │  - Product: "DISC Self-Awareness Assessment"                │    │
│  │  - Customer: John Doe                                       │    │
│  │  - Email: john@example.com                                  │    │
│  └────────────────────────────────────────────────────────────┘    │
│                             │                                        │
│                             ▼                                        │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ Razorpay Order Created with NOTES:                         │    │
│  │  {                                                          │    │
│  │    "product_id": "101",                                     │    │
│  │    "product_name": "DISC Self-Awareness Assessment",        │    │
│  │    "product_type": "disc",           ← YOU ADD THIS        │    │
│  │    "name": "John Doe",                                      │    │
│  │    "user_email": "john@example.com",                        │    │
│  │    "gender": "Male"                                         │    │
│  │  }                                                          │    │
│  └────────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   CUSTOMER PAYS VIA RAZORPAY                        │
│              (UPI / Card / Net Banking / Wallet)                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                RAZORPAY SENDS WEBHOOK TO REPLIT                     │
│                                                                     │
│  POST https://your-replit.repl.co/razorpay-webhook                 │
│  {                                                                  │
│    "event": "payment.captured",                                    │
│    "payload": {                                                    │
│      "payment": {                                                  │
│        "entity": {                                                 │
│          "amount": 525,                                            │
│          "email": "john@example.com",                              │
│          "notes": {                                                │
│            "product_type": "disc",  ← Webhook reads this           │
│            ...                                                     │
│          }                                                         │
│        }                                                           │
│      }                                                             │
│    }                                                               │
│  }                                                                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              YOUR WEBHOOK (main.py on Replit)                       │
│                                                                     │
│  1. Receives payment data                                          │
│  2. Extracts: product_id, product_name, product_type               │
│  3. Logs all details                                               │
│  4. Routes based on product_type:                                  │
│                                                                     │
│     ┌──────────────────┐              ┌──────────────────┐        │
│     │ product_type =   │              │ product_type =   │        │
│     │     "disc"       │              │   "harrason"     │        │
│     └────────┬─────────┘              └────────┬─────────┘        │
│              │                                  │                  │
│              ▼                                  ▼                  │
│     ┌──────────────────┐              ┌──────────────────┐        │
│     │  DISC Asia+ API  │              │  Harrason API    │        │
│     │  Create Account  │              │  Create Account  │        │
│     │  Get Link        │              │  Get Link        │        │
│     └────────┬─────────┘              └────────┬─────────┘        │
│              │                                  │                  │
│              └──────────────┬───────────────────┘                  │
│                             │                                      │
│                             ▼                                      │
│                  ┌─────────────────────┐                           │
│                  │   Send Email with:  │                           │
│                  │   - Login Details   │                           │
│                  │   - Assessment Link │                           │
│                  │   - Password        │                           │
│                  └─────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   CUSTOMER RECEIVES EMAIL                           │
│                                                                     │
│  Subject: Your DISC Assessment is Ready!                           │
│                                                                     │
│  Email: john@example.com                                           │
│  Password: Xy7#mK9@pL2q                                            │
│  Link: [Start Your Assessment Now]                                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Points

1. **Odoo Must Send**: `product_type` in the `notes` field
2. **Webhook Receives**: Product details from Razorpay
3. **Automatic Routing**: DISC or Harrason based on product_type
4. **Customer Gets**: Email with assessment link

## Current Issue

❌ Odoo is NOT sending product details in `notes`
✅ Once configured, webhook will automatically route correctly
