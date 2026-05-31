articles = [

    {
        "id": 1,
        "title": "VPN Troubleshooting Guide",
        "category": "network",
        "tags": ["vpn", "mfa", "authentication", "connectivity"],
        "content": (
            "If VPN login fails, first verify your internet connection is active. "
            "Check that your MFA token is valid and not expired. "
            "Re-enter your VPN credentials carefully. "
            "If the issue persists, try reinstalling the VPN client. "
            "Contact IT support if MFA enrollment needs to be reset."
        )
    },
    {
        "id": 2,
        "title": "MFA Reset Procedure",
        "category": "security",
        "tags": ["mfa", "2fa", "authentication", "reset"],
        "content": (
            "To reset MFA, log into the security portal with your manager approval. "
            "Remove your existing device from the enrolled devices list. "
            "Scan the new QR code with your authenticator app. "
            "Test the new MFA code before logging out of the portal. "
            "If you cannot access the portal, contact IT helpdesk directly."
        )
    },
    {
        "id": 3,
        "title": "Outlook Login Issues",
        "category": "email",
        "tags": ["outlook", "exchange", "email", "login"],
        "content": (
            "If Outlook cannot connect, verify Exchange server connectivity first. "
            "Check that your mailbox is active and not over quota. "
            "Re-enter your credentials in the account settings. "
            "Disable any recent add-ins that may interfere with login. "
            "For persistent issues, remove and re-add your account in Outlook."
        )
    },
    {
        "id": 4,
        "title": "Printer Troubleshooting",
        "category": "hardware",
        "tags": ["printer", "spooler", "offline", "print"],
        "content": (
            "If the printer is offline, restart the print spooler service first. "
            "Go to Services in Windows and restart Print Spooler. "
            "Check the network cable or Wi-Fi connection of the printer. "
            "Clear all pending print jobs from the queue. "
            "Reinstall the printer driver if the issue continues."
        )
    },
    {
        "id": 5,
        "title": "Network Connectivity Issues",
        "category": "network",
        "tags": ["network", "internet", "dns", "connectivity"],
        "content": (
            "If there is no internet access, restart your network adapter first. "
            "Check the router and switch status lights. "
            "Run ipconfig /release and ipconfig /renew in Command Prompt. "
            "Flush DNS cache with ipconfig /flushdns. "
            "Contact network team if multiple users are affected."
        )
    },
    {
        "id": 6,
        "title": "Account Unlock Procedure",
        "category": "account",
        "tags": ["account", "locked", "active-directory", "unlock"],
        "content": (
            "Locked accounts can be unlocked from Active Directory by IT admins. "
            "Submit a ticket with your employee ID and manager approval. "
            "Accounts are locked after 5 failed login attempts by policy. "
            "After unlock, reset your password immediately. "
            "Enable MFA to prevent future unauthorized access."
        )
    },
    {
        "id": 7,
        "title": "Password Reset Guide",
        "category": "account",
        "tags": ["password", "reset", "self-service", "credentials"],
        "content": (
            "Use the self-service password reset portal at reset.company.com. "
            "Verify your identity using your registered email or phone. "
            "Choose a strong password with at least 12 characters. "
            "Include uppercase, lowercase, numbers and special characters. "
            "Do not reuse your last 5 passwords as per company policy."
        )
    },
    {
        "id": 8,
        "title": "Email Sending Problems",
        "category": "email",
        "tags": ["email", "outlook", "exchange", "outbox"],
        "content": (
            "If emails are stuck in outbox, check Exchange server connectivity. "
            "Verify your mailbox is not over the storage quota. "
            "Try sending a test email to an internal address first. "
            "Disable email encryption add-ins temporarily for testing. "
            "Contact Exchange admin if the outbox issue affects multiple users."
        )
    },
    {
        "id": 9,
        "title": "Laptop Hardware Issues",
        "category": "hardware",
        "tags": ["laptop", "power", "hardware", "battery"],
        "content": (
            "If the laptop does not power on, check the power adapter and cable. "
            "Try a different power socket to rule out electrical issues. "
            "Hold the power button for 10 seconds to force a hard reset. "
            "Remove any external devices before powering on. "
            "Submit a hardware replacement request if the issue persists."
        )
    },
    {
        "id": 10,
        "title": "Monitor and Display Troubleshooting",
        "category": "hardware",
        "tags": ["monitor", "display", "hdmi", "screen"],
        "content": (
            "If the monitor shows no signal, check the cable connection on both ends. "
            "Try a different cable type such as HDMI or DisplayPort. "
            "Press the monitor input button to select the correct source. "
            "Test the monitor with another computer to isolate the issue. "
            "Update the graphics driver if the display is distorted."
        )
    },
]
