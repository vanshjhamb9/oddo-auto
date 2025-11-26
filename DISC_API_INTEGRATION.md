# DISC Asia+ API Integration Guide

## API Details

**Endpoint**: `https://discapi.discasiaplus.org/api/DISC/Respondent_and_Report_Details_Bodhih`

**Method**: `POST`

**Headers**: `Content-Type: application/json`

---

## Request Format

Your webhook sends this exact format to DISC API:

```json
{
  "credentials": {
    "encryptedPassword": "YOUR_DISC_CREDENTIAL"
  },
  "respondentDetails": [
    {
      "name": "test1234",
      "displayName": "test1234",
      "gender": "Male",
      "eMailAddress": "vanshjhamb9@gmail.com",
      "type": "Basic"
    }
  ],
  "transactionDetails": {
    "transactionId": 0,
    "transactionDate": "2025-11-25T12:07:35.123Z",
    "isSuccessful": true
  }
}
```

## Field Mapping

| Field | Source | Description |
|-------|--------|-------------|
| `credentials.encryptedPassword` | Replit Secret `DISC_CREDENTIAL` | Your DISC API credential |
| `respondentDetails[0].name` | Razorpay notes or Odoo customer | Respondent name |
| `respondentDetails[0].displayName` | Same as name | Display name |
| `respondentDetails[0].gender` | Razorpay notes field | Male/Female |
| `respondentDetails[0].eMailAddress` | Razorpay email field | Customer email |
| `respondentDetails[0].type` | Extracted from product name | Basic, Advanced, etc. |
| `transactionDetails.transactionId` | 0 | Always 0 for new transactions |
| `transactionDetails.transactionDate` | Current timestamp | ISO format |
| `transactionDetails.isSuccessful` | true | Always true when registering |

---

## Response Format

**Success Response:**
```json
{
  "success": true,
  "respondentDetails": [
    {
      "link": "https://discreport.discasiaplus.org/login?token=ABC123...",
      "respondentId": 12345
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "errorMessage": "Invalid credentials or respondent details"
}
```

---

## What Your Webhook Does

1. **Receives Razorpay payment** from webhook
2. **Extracts customer details**:
   - Name from Razorpay notes or customer field
   - Email from Razorpay email field
   - Gender from Razorpay notes or defaults to "Male"
   - Report type from product description (Basic, Advanced, etc.)

3. **Creates DISC API payload** with exact format above
4. **Sends POST request** to DISC API
5. **Gets assessment link** from response
6. **Sends email** to customer with assessment link

---

## Testing the API Directly (with Postman)

### Step 1: Get Your DISC Credential
- It's stored securely in Replit Secrets as `DISC_CREDENTIAL`
- Your webhook uses this automatically

### Step 2: Create Postman Request
- **Method**: POST
- **URL**: `https://discapi.discasiaplus.org/api/DISC/Respondent_and_Report_Details_Bodhih`
- **Headers**: `Content-Type: application/json`

### Step 3: Use This Body (replace with your credential):
```json
{
  "credentials": {
    "encryptedPassword": "YOUR_DISC_CREDENTIAL_HERE"
  },
  "respondentDetails": [
    {
      "name": "Test User",
      "displayName": "Test User",
      "gender": "Male",
      "eMailAddress": "test@example.com",
      "type": "Basic"
    }
  ],
  "transactionDetails": {
    "transactionId": 0,
    "transactionDate": "2025-11-25T12:07:35.123Z",
    "isSuccessful": true
  }
}
```

### Step 4: Send & Check Response
- Should see success with assessment link
- If error, check your DISC credential is correct

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `Invalid credentials` | Verify DISC_CREDENTIAL secret is correct in Replit |
| `Unable to authenticate` | Contact DISC Asia+ support to verify credential format |
| `Empty respondentDetails in response` | Check all required fields are present |
| `No assessment link returned` | Check the response structure - link should be in `respondentDetails[0].link` |

---

## Production Checklist

✅ DISC_CREDENTIAL configured in Replit Secrets
✅ API URL correct: `https://discapi.discasiaplus.org/api/DISC/Respondent_and_Report_Details_Bodhih`
✅ Request format matches exactly
✅ Response parsing looks for `respondentDetails[0].link`
✅ Error handling logs failures
✅ Email sending includes assessment link

---

## Webhook Code Location

Function: `register_on_disc_asia()` in `main.py` (lines 45-79)

This function:
1. Validates DISC credential is configured
2. Creates payload with correct format
3. Posts to DISC API
4. Extracts assessment link from response
5. Returns link to send to customer email

---

## Testing End-to-End

1. **Create Odoo sale order** with product "DISC Asia+ Basic Report"
2. **Complete Razorpay payment**
3. **Webhook automatically**:
   - Calls DISC API
   - Gets assessment link
   - Sends email to customer
4. **Check Replit logs** for "DISC SUCCESS" message
