# Odoo 18.4 SAAS - Razorpay Product Details Configuration

## Challenge with SAAS
Since you're on **Odoo SAAS**, you **cannot directly edit Python files**. You need to create a custom module or use available tools.

---

## Solution 1: Custom Module (Recommended for SAAS)

### Step 1: Contact Odoo Support or Developer
Since this is SAAS, you'll need:
- An Odoo developer to create a custom module
- Or request Odoo support to add this feature

### Step 2: Custom Module Code

Your developer should create a module that inherits `payment.transaction`:

**File: `custom_razorpay_notes/__manifest__.py`**
```python
{
    'name': 'Custom Razorpay Product Notes',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Payment Acquirers',
    'summary': 'Add product details to Razorpay payment notes',
    'depends': ['payment_razorpay', 'sale'],
    'data': [],
    'installable': True,
    'auto_install': False,
}
```

**File: `custom_razorpay_notes/models/__init__.py`**
```python
from . import payment_transaction
```

**File: `custom_razorpay_notes/models/payment_transaction.py`**
```python
from odoo import models, api

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _razorpay_prepare_payment_request_payload(self):
        """Override to add product details to notes"""
        payload = super()._razorpay_prepare_payment_request_payload()
        
        # Add product details to notes
        product_notes = self._get_product_notes_for_webhook()
        
        # Merge with existing notes
        if 'notes' in payload:
            payload['notes'].update(product_notes)
        else:
            payload['notes'] = product_notes
            
        return payload
    
    def _get_product_notes_for_webhook(self):
        """Extract product information for webhook routing"""
        self.ensure_one()
        
        # Get sale order
        sale_order = self.sale_order_ids[0] if self.sale_order_ids else None
        
        if not sale_order or not sale_order.order_line:
            return {}
        
        # Get first product line
        first_line = sale_order.order_line[0]
        product = first_line.product_id
        product_name = product.name
        
        # Determine product type based on product name/internal reference
        product_type = self._determine_product_type(product)
        
        # Get customer details
        partner = self.partner_id
        
        return {
            'product_id': str(product.id),
            'product_name': product_name,
            'product_type': product_type,
            'name': partner.name or 'Customer',
            'user_email': partner.email or '',
            'gender': self._get_partner_gender(partner),
        }
    
    def _determine_product_type(self, product):
        """Determine if product is DISC or Harrason"""
        # Check product name
        product_name_lower = product.name.lower()
        
        # Check internal reference
        product_ref = product.default_code or ''
        product_ref_lower = product_ref.lower()
        
        # Check product category
        category_name = product.categ_id.name.lower() if product.categ_id else ''
        
        # Determine type
        if 'harrason' in product_name_lower or 'harrison' in product_name_lower:
            return 'harrason'
        elif 'harrason' in product_ref_lower or 'harrison' in product_ref_lower:
            return 'harrason'
        elif 'harrason' in category_name or 'harrison' in category_name:
            return 'harrason'
        elif 'disc' in product_name_lower:
            return 'disc'
        elif 'disc' in product_ref_lower:
            return 'disc'
        elif 'disc' in category_name:
            return 'disc'
        else:
            return 'disc'  # Default to DISC
    
    def _get_partner_gender(self, partner):
        """Get partner gender if field exists"""
        if hasattr(partner, 'gender') and partner.gender:
            return partner.gender
        return 'Male'  # Default
```

---

## Solution 2: Use Product Internal Reference (Quick Fix)

This doesn't require code changes:

### Step 1: Set Product Internal References
1. Go to **Sales** → **Products** → **Products**
2. For each DISC product:
   - Set **Internal Reference**: `DISC-001`, `DISC-002`, etc.
3. For each Harrason product:
   - Set **Internal Reference**: `HARRASON-001`, `HARRASON-002`, etc.

### Step 2: Name Products Properly
Make sure product names include keywords:
- ✅ "**DISC** Self-Awareness Advanced Assessment"
- ✅ "**DISC** Leadership Report"
- ✅ "**Harrason** 360 Leadership Assessment"
- ✅ "**Harrason** Team Evaluation"

**Then the custom module above will automatically detect the type!**

---

## Solution 3: Product Categories Method

### Step 1: Create Assessment Categories
1. Go to **Sales** → **Configuration** → **Product Categories**
2. Create categories:
   - "DISC Assessments"
   - "Harrason Assessments"

### Step 2: Assign Products to Categories
1. Go to each assessment product
2. Set **Product Category** to either:
   - "DISC Assessments"
   - "Harrason Assessments"

**The custom module will detect from category names!**

---

## Solution 4: Webhook Payload Inspection (Temporary)

If you need to test immediately before custom module:

### Option A: Update Webhook to Handle Description Field
Since Odoo is currently sending `"description": "SO-05200-5"` (Sale Order number), we can:

1. Create a mapping in your webhook between Sale Order patterns and product types
2. Or configure Odoo to use product name in description field

### Option B: API-Based Solution
Create a separate API endpoint that:
1. Receives webhook
2. Queries Odoo for Sale Order details
3. Gets product information
4. Routes to correct API

---

## Recommended Path for You

Since you're on **SAAS**, here's what I recommend:

### Immediate Action:
1. **Name your products with keywords**:
   - All DISC products: Include "DISC" in the name
   - All Harrason products: Include "Harrason" in the name

2. **Set Internal References**:
   - DISC products: `DISC-*`
   - Harrason products: `HARRASON-*`

3. **Hire Odoo Developer** to install the custom module above

### Timeline:
- **Today**: Set product names and internal references
- **This Week**: Get developer to create custom module
- **Testing**: Use the test script to verify webhook receives product details

---

## Alternative: Manual Configuration via Odoo API

If you can't create custom module, you could:

1. Use Odoo API to fetch sale order details when webhook is received
2. Query product information
3. Then route to correct API

**Would you like me to create this alternative solution?**

---

## Questions for You

1. **Do you have access to Odoo Studio** in your SAAS plan?
2. **Can you install custom modules** on your SAAS instance?
3. **Do you have an Odoo developer** available?
4. **Would you prefer the API-based solution** (query Odoo from webhook)?

Let me know and I'll provide the exact solution for your situation!
