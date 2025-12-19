CARRIERS = {
    "UPS": {
        "carrier_id": "UPS",
        "name": "United Parcel Service",
        "services": ["Ground", "2nd Day Air", "Next Day Air", "Worldwide Express"],
        "tracking_url": "https://wwwapps.ups.com/tracking/tracking.cgi?tracknum=",
        "api_status": "OPERATIONAL",
        "average_delivery_time_days": 3,
        "coverage": ["US", "CA", "MX", "EU", "WORLDWIDE"]
    },
    "FedEx": {
        "carrier_id": "FedEx",
        "name": "Federal Express",
        "services": ["Ground", "Express Saver", "Priority Overnight", "International Priority"],
        "tracking_url": "https://www.fedex.com/fedextrack/?tracknumbers=",
        "api_status": "OPERATIONAL",
        "average_delivery_time_days": 2,
        "coverage": ["US", "CA", "MX", "EU", "WORLDWIDE"]
    },
    "USPS": {
        "carrier_id": "USPS",
        "name": "United States Postal Service",
        "services": ["First Class", "Priority Mail", "Priority Mail Express", "Parcel Select"],
        "tracking_url": "https://tools.usps.com/go/TrackConfirmAction?tLabels=",
        "api_status": "OPERATIONAL",
        "average_delivery_time_days": 4,
        "coverage": ["US"]
    },
    "DHL": {
        "carrier_id": "DHL",
        "name": "DHL Express",
        "services": ["Domestic Express", "International Express", "Worldwide Economy"],
        "tracking_url": "https://www.dhl.com/en/express/tracking.html?AWB=",
        "api_status": "OPERATIONAL",
        "average_delivery_time_days": 3,
        "coverage": ["EU", "US", "WORLDWIDE"]
    },
    "Royal Mail": {
        "carrier_id": "Royal Mail",
        "name": "Royal Mail",
        "services": ["First Class", "Second Class", "Special Delivery", "International Standard"],
        "tracking_url": "https://www.royalmail.com/track-your-item#/tracking-results/",
        "api_status": "DEGRADED",
        "average_delivery_time_days": 5,
        "coverage": ["GB", "EU"]
    }
}

CARRIER_INCIDENTS = {
    "2025-12-19": [
        {
            "carrier_id": "Royal Mail",
            "incident_type": "API_OUTAGE",
            "severity": "MEDIUM",
            "description": "Tracking API experiencing intermittent failures",
            "start_time": "2025-12-19T06:00:00Z",
            "expected_end_time": "2025-12-19T18:00:00Z",
            "affected_services": ["tracking_updates"],
            "workaround": "Use carrier website for tracking"
        }
    ],
    "2025-12-17": [
        {
            "carrier_id": "Royal Mail",
            "incident_type": "CUSTOMS_DELAYS",
            "severity": "HIGH",
            "description": "Customs processing experiencing significant delays",
            "start_time": "2025-12-17T00:00:00Z",
            "expected_end_time": "2025-12-21T00:00:00Z",
            "affected_services": ["international_shipments"],
            "workaround": "Inform customers of potential delays"
        }
    ],
    "2025-12-10": [
        {
            "carrier_id": "FedEx",
            "incident_type": "WEATHER_DELAYS",
            "severity": "MEDIUM",
            "description": "Winter storm causing delays in Northeast region",
            "start_time": "2025-12-10T00:00:00Z",
            "expected_end_time": "2025-12-12T23:59:59Z",
            "affected_services": ["all_services"],
            "affected_regions": ["NY", "MA", "CT", "VT", "NH", "ME"]
        }
    ]
}

TRACKING_SCANS = {
    "1Z999AA10123456784": [
        {
            "timestamp": "2025-12-17T18:02:00Z",
            "location": "San Francisco, CA",
            "status": "PICKED_UP",
            "description": "Package picked up by UPS"
        },
        {
            "timestamp": "2025-12-17T22:15:00Z",
            "location": "Oakland, CA",
            "status": "ARRIVED_AT_FACILITY",
            "description": "Arrived at UPS facility"
        },
        {
            "timestamp": "2025-12-18T02:30:00Z",
            "location": "Oakland, CA",
            "status": "DEPARTED_FACILITY",
            "description": "Departed Oakland facility"
        },
        {
            "timestamp": "2025-12-18T16:22:00Z",
            "location": "Oakland, CA",
            "status": "IN_TRANSIT",
            "description": "Departed hub"
        }
    ],
    "9400111899223856923412": [
        {
            "timestamp": "2025-12-12T09:00:00Z",
            "location": "Dallas, TX",
            "status": "PICKED_UP",
            "description": "USPS picked up package"
        },
        {
            "timestamp": "2025-12-13T14:30:00Z",
            "location": "Houston, TX",
            "status": "IN_TRANSIT",
            "description": "In transit to destination"
        },
        {
            "timestamp": "2025-12-14T08:15:00Z",
            "location": "Austin, TX",
            "status": "OUT_FOR_DELIVERY",
            "description": "Out for delivery"
        },
        {
            "timestamp": "2025-12-15T11:04:00Z",
            "location": "Austin, TX",
            "status": "DELIVERED",
            "description": "Delivered - Left at front door"
        }
    ],
    "RM123456789GB": [
        {
            "timestamp": "2025-12-14T08:00:00Z",
            "location": "London, GB",
            "status": "PICKED_UP",
            "description": "Collected by Royal Mail"
        },
        {
            "timestamp": "2025-12-15T22:00:00Z",
            "location": "Heathrow, GB",
            "status": "AT_CUSTOMS",
            "description": "Awaiting customs clearance"
        },
        {
            "timestamp": "2025-12-17T14:00:00Z",
            "location": "Heathrow, GB",
            "status": "CUSTOMS_DELAY",
            "description": "Delayed at customs - missing documentation"
        }
    ],
    "123456789012": [
        {
            "timestamp": "2025-12-18T07:30:00Z",
            "location": "San Francisco, CA",
            "status": "PICKED_UP",
            "description": "Package picked up by FedEx"
        },
        {
            "timestamp": "2025-12-18T12:00:00Z",
            "location": "Memphis, TN",
            "status": "ARRIVED_AT_HUB",
            "description": "Arrived at FedEx hub"
        },
        {
            "timestamp": "2025-12-19T02:30:00Z",
            "location": "Newark, NJ",
            "status": "DEPARTED_FACILITY",
            "description": "Departed facility"
        },
        {
            "timestamp": "2025-12-19T06:00:00Z",
            "location": "New York, NY",
            "status": "ARRIVED_AT_FACILITY",
            "description": "Arrived at local facility"
        },
        {
            "timestamp": "2025-12-19T08:00:00Z",
            "location": "New York, NY",
            "status": "OUT_FOR_DELIVERY",
            "description": "On FedEx vehicle for delivery"
        }
    ]
}

RATE_CARDS = {
    "domestic": {
        "UPS": {
            "ground": 8.99,
            "2_day": 15.99,
            "overnight": 29.99
        },
        "FedEx": {
            "ground": 8.49,
            "2_day": 14.99,
            "overnight": 27.99
        },
        "USPS": {
            "first_class": 5.99,
            "priority": 9.99,
            "express": 24.99
        }
    },
    "international": {
        "UPS": {
            "worldwide_express": 79.99,
            "worldwide_saver": 59.99
        },
        "FedEx": {
            "international_priority": 74.99,
            "international_economy": 54.99
        },
        "DHL": {
            "express": 69.99,
            "economy": 49.99
        }
    }
}

