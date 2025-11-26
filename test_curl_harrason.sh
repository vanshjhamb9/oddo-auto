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
          "id": "pay_TEST987654321",
          "amount": 1050,
          "currency": "INR",
          "status": "captured",
          "order_id": "order_TEST123456789",
          "method": "card",
          "captured": true,
          "description": "Harrason Leadership Assessment",
          "email": "test2@example.com",
          "contact": "+919876543211",
          "notes": {
            "product_id": "202",
            "product_name": "Harrason Leadership Assessment",
            "product_type": "harrason",
            "name": "Test User 2",
            "user_email": "test2@example.com",
            "gender": "Female"
          }
        }
      }
    }
  }'
