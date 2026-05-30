from datetime import datetime, timedelta

now = datetime.now()


tickets = [

    {
        "id": 1,
        "title": "VPN login failed",
        "description": "User cannot connect to VPN. MFA token is not accepted.",
        "department": "IT",
        "priority": "high",
        "tenant": "company_a",
        "created_at": (now - timedelta(minutes=5)).isoformat()
    },
    {
        "id": 2,
        "title": "VPN MFA issue",
        "description": "VPN connection drops after MFA step. Credentials seem correct.",
        "department": "IT",
        "priority": "high",
        "tenant": "company_a",
        "created_at": (now - timedelta(minutes=10)).isoformat()
    },
    {
        "id": 3,
        "title": "Cannot connect to VPN",
        "description": "VPN client shows error after entering MFA code. Internet works fine.",
        "department": "IT",
        "priority": "high",
        "tenant": "company_a",
        "created_at": (now - timedelta(minutes=20)).isoformat()
    },
    {
        "id": 4,
        "title": "VPN authentication error",
        "description": "Getting authentication failed on VPN. MFA enrollment may be broken.",
        "department": "IT",
        "priority": "medium",
        "tenant": "company_b",
        "created_at": (now - timedelta(hours=2)).isoformat()
    },

    {
        "id": 5,
        "title": "Outlook login problem",
        "description": "User cannot login to Outlook. Exchange server shows connection error.",
        "department": "Support",
        "priority": "medium",
        "tenant": "company_a",
        "created_at": (now - timedelta(hours=1)).isoformat()
    },
    {
        "id": 6,
        "title": "Email not working",
        "description": "Outlook keeps asking for password. Mailbox status shows disconnected.",
        "department": "Support",
        "priority": "medium",
        "tenant": "company_a",
        "created_at": (now - timedelta(hours=3)).isoformat()
    },
    {
        "id": 7,
        "title": "Cannot send emails",
        "description": "Outlook connected but emails stuck in outbox. Exchange sync failing.",
        "department": "Support",
        "priority": "low",
        "tenant": "company_b",
        "created_at": (now - timedelta(hours=5)).isoformat()
    },

    {
        "id": 8,
        "title": "Printer offline",
        "description": "Office printer shows offline. Print spooler service may be stuck.",
        "department": "Operations",
        "priority": "low",
        "tenant": "company_a",
        "created_at": (now - timedelta(hours=4)).isoformat()
    },
    {
        "id": 9,
        "title": "Cannot print documents",
        "description": "Print jobs queued but nothing prints. Restarting spooler did not help.",
        "department": "Operations",
        "priority": "low",
        "tenant": "company_b",
        "created_at": (now - timedelta(hours=6)).isoformat()
    },

    {
        "id": 10,
        "title": "No internet access",
        "description": "User has no internet connection. Network adapter shows connected but no traffic.",
        "department": "IT",
        "priority": "high",
        "tenant": "company_a",
        "created_at": (now - timedelta(hours=1)).isoformat()
    },
    {
        "id": 11,
        "title": "Slow network connection",
        "description": "Network is very slow. File transfers to shared drive taking too long.",
        "department": "IT",
        "priority": "medium",
        "tenant": "company_b",
        "created_at": (now - timedelta(hours=7)).isoformat()
    },

    {
        "id": 12,
        "title": "Account locked",
        "description": "User account locked after multiple failed login attempts. Needs unlock.",
        "department": "HR",
        "priority": "medium",
        "tenant": "company_a",
        "created_at": (now - timedelta(hours=2)).isoformat()
    },
    {
        "id": 13,
        "title": "Password reset request",
        "description": "User forgot password and cannot login. Needs password reset from admin.",
        "department": "HR",
        "priority": "low",
        "tenant": "company_b",
        "created_at": (now - timedelta(hours=8)).isoformat()
    },

    {
        "id": 14,
        "title": "Laptop not turning on",
        "description": "User laptop does not power on. Charging light is off.",
        "department": "Operations",
        "priority": "high",
        "tenant": "company_a",
        "created_at": (now - timedelta(hours=3)).isoformat()
    },
    {
        "id": 15,
        "title": "Monitor display issue",
        "description": "External monitor shows no signal. Cable and port seem fine.",
        "department": "Operations",
        "priority": "low",
        "tenant": "company_b",
        "created_at": (now - timedelta(hours=9)).isoformat()
    },
]
