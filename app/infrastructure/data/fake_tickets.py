from datetime import datetime, timedelta


tickets = [

    {
        "id": 1,

        "title": "VPN وصل نمیشه",

        "description":
            "کاربر نمیتونه به VPN متصل شود",

        "department": "IT",

        "priority": "high",

        "tenant": "company_a",

        "created_at":
            datetime.now() - timedelta(minutes=5)
    },

    {
        "id": 2,

        "title": "VPN authentication failed",

        "description":
            "خطای MFA دریافت میشود",

        "department": "IT",

        "priority": "high",

        "tenant": "company_a",

        "created_at":
            datetime.now() - timedelta(minutes=8)
    },

    {
        "id": 3,

        "title": "حقوق این ماه اشتباه است",

        "description":
            "salary calculation مشکل دارد",

        "department": "HR",

        "priority": "medium",

        "tenant": "company_a",

        "created_at":
            datetime.now() - timedelta(minutes=20)
    },

    {
        "id": 4,

        "title": "پرینتر آفلاین شده",

        "description":
            "printer در طبقه دوم کار نمیکند",

        "department": "IT",

        "priority": "low",

        "tenant": "company_b",

        "created_at":
            datetime.now() - timedelta(hours=2)
    }
]
