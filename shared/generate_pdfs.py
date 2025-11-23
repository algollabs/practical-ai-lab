from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os

DATA_DIR = "lab1_rag/data"
os.makedirs(DATA_DIR, exist_ok=True)

def create_pdf(filename, title, content):
    filepath = os.path.join(DATA_DIR, filename)
    c = canvas.Canvas(filepath, pagesize=LETTER)
    width, height = LETTER
    
    # Text configuration
    left_margin = 50
    top_margin = height - 50
    line_height = 14
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(left_margin, top_margin, title)
    
    c.setFont("Helvetica", 10)
    text_y = top_margin - 30
    
    # Process content line by line
    for line in content.split('\n'):
        # Check if we need a new page
        if text_y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            text_y = height - 50
            
        c.drawString(left_margin, text_y, line.strip())
        text_y -= line_height
            
    c.save()
    print(f"Created {filepath}")

policies = [
    {
        "filename": "policy_01_wfh.pdf",
        "title": "Policy 01: Work from Home (WFH) & Hybrid Work",
        "content": """
        Effective Date: January 1, 2024
        Document Owner: Human Resources
        Version: 2.0
        
        1. Purpose and Scope
        Practical AI Corp recognizes the changing nature of work and is committed to supporting flexible work arrangements. This policy outlines the guidelines, eligibility, and expectations for employees working from home (WFH) or participating in the hybrid work model. This policy applies to all full-time and part-time employees, subject to role suitability.
        
        2. Eligibility & Suitability
        2.1 Tenure Requirement
        New employees are eligible for hybrid work arrangements after successfully completing their first 30 days of employment. During the initial 30-day onboarding period, employees are expected to be in the office 5 days a week to facilitate training and cultural integration.
        
        2.2 Performance Standards
        Eligibility is contingent upon maintaining a "Meets Expectations" or higher rating in the most recent performance review. Employees on a Performance Improvement Plan (PIP) may have WFH privileges suspended until performance targets are met.
        
        2.3 Role Suitability
        Not all roles are suitable for remote work. Roles requiring physical presence (e.g., Office Management, Hardware Lab Technicians) may be ineligible or have limited WFH options.
        
        3. Hybrid Schedule & Availability
        3.1 Core Office Days
        - Employees are expected to be physically present in the office at least 3 days per week.
        - Team Leads have the discretion to designate specific "Anchor Days" where the entire team must be present.
        - Standard remote days are generally Monday and Friday, but this is subject to manager approval and business needs.
        
        3.2 Core Collaboration Hours
        To ensure synchronous collaboration, all employees (remote or onsite) must be available during Core Collaboration Hours: 10:00 AM to 3:00 PM local time. During these hours, response times to Slack messages and emails should be within 30 minutes.
        
        4. Workspace & Equipment
        4.1 Workspace Requirements
        Employees working remotely must ensure they have a dedicated, quiet workspace free from distractions. The workspace must have a reliable high-speed internet connection (minimum 50 Mbps down / 10 Mbps up).
        
        4.2 Company Equipment
        - The company provides a standard issue laptop (MacBook Pro or Dell XPS).
        - A one-time Home Office Stipend of $500 is available for permanent employees to purchase ergonomic equipment (monitors, chairs, desks).
        - All company equipment must be returned upon termination of employment.
        
        5. Data Security & Confidentiality
        - Work must only be conducted on company-issued devices. Personal devices should not be used for accessing internal systems without explicit IT approval.
        - Employees must ensure their home Wi-Fi network is secured with WPA2 or WPA3 encryption.
        - Confidential conversations should not be held in public places or near smart speakers/listening devices.
        - Lock your screen whenever you step away from your computer, even at home.
        
        6. Health, Safety, and Dependent Care
        - Employees are responsible for maintaining a safe home work environment. Practical AI Corp is not liable for injuries occurring in the home office that are not directly related to the performance of job duties.
        - WFH is not a substitute for dependent care. Employees must have adequate childcare or eldercare arrangements in place during working hours.
        
        7. Revocation of Privileges
        WFH is a privilege, not a right. Management reserves the right to revoke or modify remote work arrangements at any time due to performance issues, changing business needs, or failure to comply with this policy.
        """
    },
    {
        "filename": "policy_02_expenses.pdf",
        "title": "Policy 02: Global Expense & Reimbursement Policy",
        "content": """
        Effective Date: January 1, 2024
        Document Owner: Finance Department
        Version: 3.1
        
        1. General Principles
        Practical AI Corp reimburses employees for reasonable and necessary expenses incurred while conducting company business. Employees are expected to exercise good judgment ("act like an owner") and spend company funds prudently.
        
        2. Travel Policy
        2.1 Air Travel
        - Domestic flights (< 6 hours) must be booked in Economy Class.
        - International flights (> 8 hours) may be booked in Premium Economy.
        - Business Class is only permitted for executive leadership or with written pre-approval from the CFO.
        - Flights should be booked at least 14 days in advance whenever possible to secure the best rates.
        
        2.2 Lodging
        - Maximum nightly rates (excluding taxes):
          * Tier 1 Cities (SF, NYC, London, Tokyo): $300/night
          * Tier 2 Cities (Austin, Chicago, Berlin): $250/night
          * All other locations: $150/night
        - Airbnb/Vrbo is permitted if the total cost is lower than a comparable hotel.
        
        2.3 Ground Transportation
        - Use public transit, Uber/Lyft, or taxis.
        - Rental cars should only be booked if public transport/rideshare is cost-prohibitive or unavailable. Compact or Intermediate class vehicles only.
        - Personal Mileage: Reimbursed at the current IRS standard rate for business miles driven. Gas is not reimbursed separately for personal cars.
        
        3. Meals & Entertainment
        3.1 Individual Meals
        - Daily Allowance (Per Diem limit): $75 per day while traveling.
        - Breakfast: $15 | Lunch: $20 | Dinner: $40.
        
        3.2 Team Meals
        - Team lunches/dinners must be approved by a Director level or above.
        - Limit: $35 per person (lunch), $60 per person (dinner).
        
        3.3 Client Entertainment
        - Reasonable expenses for entertaining clients are reimbursable.
        - Alcohol is permitted but should be kept moderate.
        - VP approval required for events exceeding $500 total.
        
        4. Non-Reimbursable Expenses
        The following are strictly non-reimbursable:
        - Traffic or parking tickets.
        - Personal grooming/toiletry items.
        - In-flight Wi-Fi (unless critical for urgent business).
        - Minibar purchases.
        - Airline club memberships or lounge access.
        - Commuting costs between home and the primary office.
        
        5. Expense Submission & Reimbursement
        5.1 Receipts
        - Receipts are required for any single expense over $25.
        - Receipts must be itemized (credit card slips showing only the total are not accepted).
        
        5.2 Submission Deadline
        - Expenses must be submitted via the 'Expensify' portal within 30 days of the expense date.
        - Expenses submitted after 60 days will be considered taxable income or may be rejected.
        
        5.3 Approval Workflow
        - Expenses < $1,000: Direct Manager approval.
        - Expenses > $1,000: Manager + Department Head approval.
        
        6. Audits
        All expense reports are subject to random audits by the Finance team. Fraudulent claims will result in disciplinary action, up to and including termination.
        """
    },
    {
        "filename": "policy_03_security.pdf",
        "title": "Policy 03: IT Security, Data Protection & Compliance",
        "content": """
        Effective Date: January 1, 2024
        Document Owner: CISO (Chief Information Security Officer)
        Version: 4.2
        
        1. Password & Authentication Standards
        1.1 Password Complexity
        - Minimum length: 14 characters (expanded from previous 12).
        - Must contain a mix of uppercase, lowercase, numbers, and special symbols.
        - Passwords must not contain common dictionary words or personal info (e.g., "Password123", "PracticalAI").
        
        1.2 Rotation & History
        - Passwords must be rotated every 90 days.
        - You cannot reuse the last 5 passwords.
        
        1.3 Multi-Factor Authentication (MFA)
        - MFA is MANDATORY for all internal systems including Google Workspace, AWS, GitHub, Slack, and HR portals.
        - Hardware keys (YubiKeys) or TOTP apps (Google Authenticator, Authy) are the only approved methods. SMS-based MFA is prohibited due to SIM-swapping risks.
        
        2. Device Security (Endpoint Protection)
        2.1 Encryption
        - All company laptops must have Full Disk Encryption enabled (FileVault for Mac, BitLocker for Windows).
        - Mobile devices accessing company email must be enrolled in MDM (Mobile Device Management).
        
        2.2 Physical Security
        - Screen lock must be set to activate after a maximum of 5 minutes of inactivity.
        - Devices must never be left unattended in public vehicles or spaces.
        - Lost or stolen devices must be reported to IT Security immediately (within 1 hour).
        
        2.3 Software Installation
        - Users do not have local Admin rights by default.
        - Only software from the "Self Service" portal or approved by IT may be installed.
        - Shadow IT (unapproved SaaS tools) is strictly prohibited.
        
        3. Data Handling & Classification
        3.1 Data Classification Levels
        - Public: Marketing materials, job descriptions.
        - Internal: Policies, memos, org charts.
        - Confidential: Customer lists, pricing strategies, source code.
        - Restricted: PII (Personally Identifiable Information), financial records, private keys.
        
        3.2 Storage & Transfer
        - Customer data must NEVER be stored on local laptop drives. It must remain in approved cloud databases (AWS RDS, S3) with appropriate access controls.
        - Do not use personal email or personal cloud storage (Dropbox, GDrive) for company data.
        - Sensitive credentials (API keys, passwords) must be shared via 1Password, never via Slack or Email.
        
        4. Acceptable Use
        - Company devices are tools for business. Incidental personal use is permitted if it does not interfere with productivity or security.
        - Accessing illegal, adult, or gambling content is strictly prohibited and is grounds for immediate termination.
        - Do not connect unknown USB drives or peripherals to company machines.
        
        5. Incident Response
        - If you suspect a breach, phishing attempt, or malware infection, disconnect from the network and contact the Security Operations Center (SOC) at security@practical-ai.com or via the emergency hotline.
        - Do not attempt to investigate the breach yourself.
        
        6. Remote Access (VPN)
        - Access to internal staging/production environments requires connection via the corporate VPN (WireGuard).
        - VPN access is logged and monitored for anomalous behavior.
        """
    }
]

if __name__ == "__main__":
    print("Generating expanded policy PDFs...")
    for policy in policies:
        create_pdf(policy["filename"], policy["title"], policy["content"])
    print("Done.")
