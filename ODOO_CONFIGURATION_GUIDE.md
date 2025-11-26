# Odoo Configuration Guide for Razorpay Product Details

## Overview
Configure your Odoo Razorpay integration to send product information (product_id, product_name, product_type) in the webhook payload so the automation can route to the correct assessment API.

---

## Method 1: Using Odoo Payment Acquirer Configuration (Recommended)

### Step 1: Access Razorpay Payment Acquirer Settings

1. Go to **Accounting** or **Website** → **Configuration** → **Payment Acquirers**
2. Find and open **Razorpay** payment acquirer
3. Click **Edit**

### Step 2: Modify Razorpay Integration Code

You need to customize the Razorpay payment acquirer module. This is typically in:
- Module: `payment_razorpay` or custom Razorpay module
- File: `models/payment_transaction.py` or `controllers/main.py`

### Step 3: Add Product Details to Notes Field

In the Razorpay order creation function, modify it to include product details:

```python
# Find the function that creates Razorpay orders
# Usually named: _razorpay_create_order() or similar

def _razorpay_create_order(self):
    # Existing code...
    sale_order = self.sale_order_ids[0] if self.sale_order_ids else None
    
    # Get product information from the sale order
    product_info = {}
    if sale_order and sale_order.order_line:
        first_product = sale_order.order_line[0].product_id
        product_name = first_product.name
        
        # Determine product type based on product name/category
        product_type = "disc"  # Default
        if "harrason" in product_name.lower() or "harrison" in product_name.lower():
            product_type = "harrason"
        elif "disc" in product_name.lower():
            product_type = "disc"
        
        product_info = {
            "product_id": str(first_product.id),
            "product_name": product_name,
            "product_type": product_type,
            "name": self.partner_id.name or "Customer",
            "user_email": self.partner_id.email or "",
            "gender": self.partner_id.gender if hasattr(self.partner_id, 'gender') else "Male"
        }
    
    # Create Razorpay order with notes
    razorpay_order = self.razorpay_client.order.create({
        "amount": int(self.amount * 100),  # Amount in paise
        "currency": self.currency_id.name,
        "receipt": self.reference,
        "notes": product_info  # ← ADD THIS LINE
    })
    
    return razorpay_order
```

---

## Method 2: Using Product Categories/Tags

If you want automatic detection based on product setup:

### Step 1: Tag Products in Odoo

1. Go to **Sales** → **Products** → **Products**
2. Open each assessment product (DISC, Harrason, etc.)
3. Add a custom field or use **Internal Category**:
   - For DISC products: Add tag "disc_assessment"
   - For Harrason products: Add tag "harrason_assessment"

### Step 2: Modify Payment Flow to Read Tags

```python
def _get_product_type_from_tags(self, product):
    """Determine product type from product tags or categories"""
    product_name_lower = product.name.lower()
    
    # Check product categories
    if product.categ_id:
        category_name = product.categ_id.name.lower()
        if "harrason" in category_name or "harrison" in category_name:
            return "harrason"
        if "disc" in category_name:
            return "disc"
    
    # Check product name
    if "harrason" in product_name_lower or "harrison" in product_name_lower:
        return "harrason"
    if "disc" in product_name_lower:
        return "disc"
    
    # Default
    return "disc"
```

---

## Method 3: Quick Fix - Using Product Internal Reference

If you can't modify code, use product **Internal Reference** field:

### Step 1: Set Internal References
1. Go to each product in Odoo
2. Set **Internal Reference**:
   - DISC products: `DISC-001`, `DISC-002`, etc.
   - Harrason products: `HARRASON-001`, `HARRASON-002`, etc.

### Step 2: Modify Razorpay Integration
```python
# In your payment processing code
product_ref = sale_order.order_line[0].product_id.default_code  # Internal reference

product_type = "disc"  # Default
if product_ref and "HARRASON" in product_ref.upper():
    product_type = "harrason"
elif product_ref and "DISC" in product_ref.upper():
    product_type = "disc"

notes = {
    "product_id": str(first_product.id),
    "product_name": first_product.name,
    "product_type": product_type,
    "name": partner.name,
    "user_email": partner.email,
    "gender": getattr(partner, 'gender', 'Male')
}
```

---

## Method 4: Using Odoo Studio (No Code Solution)

If you have **Odoo Studio** (Enterprise):

### Step 1: Add Custom Field to Product
1. Open **Studio**
2. Go to **Products** model
3. Add a new field: `assessment_type` (Selection field)
4. Options: `disc`, `harrason`

### Step 2: Add Custom Field to Payment Transaction
1. In Studio, go to **Payment Transactions** model
2. Add computed field that gets product type from sale order

### Step 3: Override Razorpay API Call
Use Studio automation to populate the `notes` field before API call.

---

## Testing Your Configuration

After configuring Odoo, test with a purchase:

1. Create a test sale order with a DISC product
2. Process payment through Razorpay
3. Check your webhook logs at: `https://your-replit-url.repl.co`
4. Verify the logs show:
   ```
   Product ID     : 101
   Product Name   : DISC Self-Awareness Advanced
   Product Type   : disc
   ```

---

## Example: Complete Integration Code

Here's a complete example for your Razorpay payment transaction model:

```python
from odoo import models, fields, api

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    
    def _prepare_razorpay_order_values(self):
        """Prepare Razorpay order values with product details"""
        self.ensure_one()
        
        # Get sale order and product details
        sale_order = self.sale_order_ids[0] if self.sale_order_ids else None
        product_info = self._get_product_info_for_webhook(sale_order)
        
        return {
            'amount': int(self.amount * 100),
            'currency': self.currency_id.name,
            'receipt': self.reference,
            'notes': product_info,  # Product details for webhook
        }
    
    def _get_product_info_for_webhook(self, sale_order):
        """Extract product information for webhook routing"""
        if not sale_order or not sale_order.order_line:
            return {}
        
        # Get first product (or combine multiple products if needed)
        product = sale_order.order_line[0].product_id
        product_name = product.name
        
        # Determine assessment type
        product_type = "disc"  # Default to DISC
        if any(keyword in product_name.lower() for keyword in ["harrason", "harrison"]):
            product_type = "harrason"
        
        # Get customer details
        partner = self.partner_id
        
        return {
            "product_id": str(product.id),
            "product_name": product_name,
            "product_type": product_type,
            "name": partner.name or "Customer",
            "user_email": partner.email or "",
            "gender": partner.gender if hasattr(partner, 'gender') else "Male"
        }
```

---

## Where to Find Razorpay Code in Odoo

Common locations:
- `/odoo/addons/payment_razorpay/models/payment_transaction.py`
- `/odoo/addons/payment_razorpay/controllers/main.py`
- Custom module: `/your_custom_modules/payment_custom/models/`

---

## Need Help?

If you need assistance implementing this:
1. Share your Odoo version (Community/Enterprise)
2. Share if you have developer access
3. Share if you're using a custom Razorpay module

I can provide more specific code based on your setup!
