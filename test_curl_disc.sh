#!/bin/bash
curl -X POST http://localhost:5000/razorpay-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "entity": "event",
    "account_id": "acc_PtxbfWAGj8D2mC",
    "event": "payment.captured",
    "contains": ["payment"],
    "payload": {
      "payment": {
        "entity": {
          "id": "pay_TEST123456789",
          "amount": 525,
          "currency": "INR",
          "status": "captured",
          "order_id": "order_TEST987654321",
          "method": "upi",
          "captured": true,
          "description": "DISC Self-Awareness Advanced Report",
          "email": "test@example.com",
          "contact": "+919876543210",
          "notes": {
            "product_id": "101",
            "product_name": "DISC Self-Awareness Advanced Assessment",
            "product_type": "disc",
            "name": "Test User",
            "user_email": "test@example.com",
            "gender": "Male"
          }
        }
      }
    }
  }'
