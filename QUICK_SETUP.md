# Quick Setup Reference

## What You Need to Do in Odoo

Add this code to your Razorpay payment integration to send product details:

### Location
Find your Razorpay payment code in Odoo:
- **File**: `payment_razorpay/models/payment_transaction.py`
- **Function**: Look for where Razorpay order is created (usually has `order.create()`)

### Code to Add

```python
# When creating Razorpay order, add the notes field:

# Get product from sale order
sale_order = self.sale_order_ids[0] if self.sale_order_ids else None
product = sale_order.order_line[0].product_id if sale_order and sale_order.order_line else None

# Determine product type
product_type = "disc"  # Default
if product:
    if "harrason" in product.name.lower():
        product_type = "harrason"
    elif "disc" in product.name.lower():
        product_type = "disc"

# Create notes dictionary
notes = {
    "product_id": str(product.id) if product else "",
    "product_name": product.name if product else "",
    "product_type": product_type,
    "name": self.partner_id.name or "Customer",
    "user_email": self.partner_id.email or "",
    "gender": getattr(self.partner_id, 'gender', 'Male')
}

# Add notes to Razorpay order
razorpay_order = client.order.create({
    "amount": int(self.amount * 100),
    "currency": self.currency_id.name,
    "receipt": self.reference,
    "notes": notes  # ← ADD THIS
})
```

---

## Product Naming Convention

For automatic detection, name your products:
- ✅ "DISC Self-Awareness Assessment"
- ✅ "DISC Leadership Report"
- ✅ "Harrason 360 Assessment"
- ✅ "Harrason Leadership Evaluation"

The webhook automatically detects "disc" or "harrason" in the product name.

---

## Testing

After configuration, purchase any product and check webhook logs at:
```
https://your-replit-url.repl.co
```

You should see:
```
Product ID     : 123
Product Name   : DISC Assessment
Product Type   : disc
```

---

## Need Help?

Tell me:
1. Your Odoo version (14, 15, 16, 17?)
2. Do you have developer access?
3. Are you using custom Razorpay module or standard one?

I can provide exact code for your version!
