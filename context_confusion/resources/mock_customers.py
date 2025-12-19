CUSTOMERS = {
    "cust_123": {
        "customer_id": "cust_123",
        "email": "user@example.com",
        "name": "Avery Chen",
        "tier": "gold",
        "phone": "+1-555-0101",
        "address": {
            "street": "123 Main St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94102",
            "country": "US"
        },
        "location": "US",
        "preferred_carrier": "UPS",
        "account_status": "active"
    },
    "cust_456": {
        "customer_id": "cust_456",
        "email": "buyer@acme.com",
        "name": "Jordan Patel",
        "tier": "standard",
        "phone": "+1-555-0102",
        "address": {
            "street": "456 Oak Ave",
            "city": "Austin",
            "state": "TX",
            "zip": "78701",
            "country": "US"
        },
        "location": "US",
        "preferred_carrier": "FedEx",
        "account_status": "active"
    },
    "cust_789": {
        "customer_id": "cust_789",
        "email": "ops@widget.io",
        "name": "Sam Rivera",
        "tier": "platinum",
        "phone": "+1-555-0103",
        "address": {
            "street": "789 Enterprise Blvd",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101",
            "country": "US"
        },
        "location": "US",
        "preferred_carrier": "UPS",
        "account_status": "active"
    },
    "cust_321": {
        "customer_id": "cust_321",
        "email": "manager@euro-corp.eu",
        "name": "Alex Schmidt",
        "tier": "gold",
        "phone": "+49-555-0104",
        "address": {
            "street": "10 Hauptstraße",
            "city": "Berlin",
            "state": "BE",
            "zip": "10115",
            "country": "DE"
        },
        "location": "EU",
        "preferred_carrier": "DHL",
        "account_status": "active"
    },
    "cust_654": {
        "customer_id": "cust_654",
        "email": "buyer@uk-shop.co.uk",
        "name": "Morgan Davies",
        "tier": "standard",
        "phone": "+44-555-0105",
        "address": {
            "street": "25 Oxford Street",
            "city": "London",
            "state": "LDN",
            "zip": "W1D 2DW",
            "country": "GB"
        },
        "location": "EU",
        "preferred_carrier": "Royal Mail",
        "account_status": "active"
    },
    "cust_987": {
        "customer_id": "cust_987",
        "email": "vip@luxury-goods.com",
        "name": "Taylor Kim",
        "tier": "platinum",
        "phone": "+1-555-0106",
        "address": {
            "street": "1 Park Avenue",
            "city": "New York",
            "state": "NY",
            "zip": "10016",
            "country": "US"
        },
        "location": "US",
        "preferred_carrier": "FedEx",
        "account_status": "active"
    },
    "cust_111": {
        "customer_id": "cust_111",
        "email": "support@startup.io",
        "name": "Casey Johnson",
        "tier": "standard",
        "phone": "+1-555-0107",
        "address": {
            "street": "500 Tech Drive",
            "city": "San Jose",
            "state": "CA",
            "zip": "95110",
            "country": "US"
        },
        "location": "US",
        "preferred_carrier": "USPS",
        "account_status": "active"
    }
}

CUSTOMER_EMAIL_MAP = {
    "user@example.com": "cust_123",
    "buyer@acme.com": "cust_456",
    "ops@widget.io": "cust_789",
    "manager@euro-corp.eu": "cust_321",
    "buyer@uk-shop.co.uk": "cust_654",
    "vip@luxury-goods.com": "cust_987",
    "support@startup.io": "cust_111"
}

CUSTOMER_PREFERENCES = {
    "cust_123": {
        "signature_required": True,
        "delivery_instructions": "Leave at front desk",
        "email_notifications": True,
        "sms_notifications": True
    },
    "cust_456": {
        "signature_required": False,
        "delivery_instructions": "Ring doorbell",
        "email_notifications": True,
        "sms_notifications": False
    },
    "cust_789": {
        "signature_required": True,
        "delivery_instructions": "Deliver to loading dock",
        "email_notifications": True,
        "sms_notifications": True
    },
    "cust_321": {
        "signature_required": True,
        "delivery_instructions": "Call before delivery",
        "email_notifications": True,
        "sms_notifications": True
    },
    "cust_654": {
        "signature_required": False,
        "delivery_instructions": "Leave with neighbor",
        "email_notifications": True,
        "sms_notifications": False
    },
    "cust_987": {
        "signature_required": True,
        "delivery_instructions": "Concierge delivery only",
        "email_notifications": True,
        "sms_notifications": True
    },
    "cust_111": {
        "signature_required": False,
        "delivery_instructions": "Front door",
        "email_notifications": True,
        "sms_notifications": False
    }
}

BILLING_INFO = {
    "cust_123": {
        "billing_id": "bill_124",
        "payment_method": "credit_card",
        "credit_balance": 0.0
    },
    "cust_456": {
        "billing_id": "bill_457",
        "payment_method": "paypal",
        "credit_balance": 25.00
    },
    "cust_789": {
        "billing_id": "bill_790",
        "payment_method": "corporate_account",
        "credit_balance": 150.00
    },
    "cust_321": {
        "billing_id": "bill_322",
        "payment_method": "credit_card",
        "credit_balance": 0.0
    },
    "cust_654": {
        "billing_id": "bill_655",
        "payment_method": "debit_card",
        "credit_balance": 10.00
    },
    "cust_987": {
        "billing_id": "bill_988",
        "payment_method": "credit_card",
        "credit_balance": 500.00
    },
    "cust_111": {
        "billing_id": "bill_112",
        "payment_method": "credit_card",
        "credit_balance": 0.0
    }
}

