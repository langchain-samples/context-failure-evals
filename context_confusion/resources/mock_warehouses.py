WAREHOUSES = {
    "WH-01": {
        "warehouse_id": "WH-01",
        "name": "San Francisco Distribution Center",
        "location": {
            "city": "San Francisco",
            "state": "CA",
            "zip": "94110",
            "country": "US"
        },
        "capacity": 50000,
        "current_inventory": 32450,
        "status": "OPERATIONAL",
        "carriers": ["UPS", "FedEx", "USPS"],
        "operating_hours": "24/7"
    },
    "WH-02": {
        "warehouse_id": "WH-02",
        "name": "Dallas Fulfillment Center",
        "location": {
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "country": "US"
        },
        "capacity": 35000,
        "current_inventory": 28900,
        "status": "OPERATIONAL",
        "carriers": ["USPS", "FedEx"],
        "operating_hours": "Mon-Sat 6AM-10PM"
    },
    "WH-03": {
        "warehouse_id": "WH-03",
        "name": "Chicago Regional Hub",
        "location": {
            "city": "Chicago",
            "state": "IL",
            "zip": "60601",
            "country": "US"
        },
        "capacity": 40000,
        "current_inventory": 15670,
        "status": "MAINTENANCE",
        "carriers": ["UPS", "FedEx"],
        "operating_hours": "Currently closed for maintenance"
    },
    "WH-EU-01": {
        "warehouse_id": "WH-EU-01",
        "name": "Amsterdam European Hub",
        "location": {
            "city": "Amsterdam",
            "state": "NH",
            "zip": "1012",
            "country": "NL"
        },
        "capacity": 30000,
        "current_inventory": 22100,
        "status": "OPERATIONAL",
        "carriers": ["DHL", "FedEx"],
        "operating_hours": "24/7"
    },
    "WH-UK-01": {
        "warehouse_id": "WH-UK-01",
        "name": "London Distribution Center",
        "location": {
            "city": "London",
            "state": "LDN",
            "zip": "E14 5AB",
            "country": "GB"
        },
        "capacity": 25000,
        "current_inventory": 18900,
        "status": "OPERATIONAL",
        "carriers": ["Royal Mail", "DHL"],
        "operating_hours": "Mon-Fri 7AM-8PM"
    }
}

INVENTORY = {
    "SKU-123": {
        "sku": "SKU-123",
        "name": "Premium Widget",
        "stock_by_warehouse": {
            "WH-01": 150,
            "WH-02": 80,
            "WH-03": 45
        },
        "total_stock": 275,
        "reorder_threshold": 50,
        "status": "IN_STOCK"
    },
    "SKU-777": {
        "sku": "SKU-777",
        "name": "Standard Gadget",
        "stock_by_warehouse": {
            "WH-01": 320,
            "WH-02": 280,
            "WH-03": 190
        },
        "total_stock": 790,
        "reorder_threshold": 100,
        "status": "IN_STOCK"
    },
    "SKU-ENT-1": {
        "sku": "SKU-ENT-1",
        "name": "Enterprise Solution",
        "stock_by_warehouse": {
            "WH-01": 25,
            "WH-02": 15
        },
        "total_stock": 40,
        "reorder_threshold": 10,
        "status": "IN_STOCK"
    },
    "SKU-456": {
        "sku": "SKU-456",
        "name": "European Widget",
        "stock_by_warehouse": {
            "WH-EU-01": 200,
            "WH-UK-01": 100
        },
        "total_stock": 300,
        "reorder_threshold": 75,
        "status": "IN_STOCK"
    },
    "SKU-UK-1": {
        "sku": "SKU-UK-1",
        "name": "UK Widget",
        "stock_by_warehouse": {
            "WH-UK-01": 150
        },
        "total_stock": 150,
        "reorder_threshold": 50,
        "status": "IN_STOCK"
    },
    "SKU-LUX-1": {
        "sku": "SKU-LUX-1",
        "name": "Luxury Item",
        "stock_by_warehouse": {
            "WH-01": 30,
            "WH-EU-01": 20
        },
        "total_stock": 50,
        "reorder_threshold": 15,
        "status": "IN_STOCK"
    },
    "SKU-999": {
        "sku": "SKU-999",
        "name": "Basic Widget",
        "stock_by_warehouse": {
            "WH-01": 500,
            "WH-02": 450,
            "WH-03": 350,
            "WH-UK-01": 200
        },
        "total_stock": 1500,
        "reorder_threshold": 200,
        "status": "IN_STOCK"
    },
    "SKU-OOS-1": {
        "sku": "SKU-OOS-1",
        "name": "Out of Stock Item",
        "stock_by_warehouse": {},
        "total_stock": 0,
        "reorder_threshold": 100,
        "status": "OUT_OF_STOCK",
        "expected_restock_date": "2025-12-30"
    }
}

WAREHOUSE_INCIDENTS = {
    "2025-12-18": [
        {
            "warehouse_id": "WH-03",
            "incident_type": "MAINTENANCE",
            "severity": "MEDIUM",
            "description": "Scheduled HVAC maintenance",
            "start_time": "2025-12-18T00:00:00Z",
            "expected_end_time": "2025-12-22T00:00:00Z",
            "impact": "Reduced order processing capacity"
        }
    ],
    "2025-12-15": [
        {
            "warehouse_id": "WH-02",
            "incident_type": "POWER_OUTAGE",
            "severity": "HIGH",
            "description": "Brief power outage affected systems",
            "start_time": "2025-12-15T14:00:00Z",
            "expected_end_time": "2025-12-15T16:30:00Z",
            "impact": "2-hour delay in order processing"
        }
    ]
}

