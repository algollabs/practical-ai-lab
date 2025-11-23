from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import os

DATA_DIR = "lab1_rag/data"
os.makedirs(DATA_DIR, exist_ok=True)

def create_pdf(filename, title, content):
    filepath = os.path.join(DATA_DIR, filename)
    c = canvas.Canvas(filepath, pagesize=LETTER)
    width, height = LETTER
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, title)
    
    c.setFont("Helvetica", 12)
    text_object = c.beginText(50, height - 80)
    for line in content.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    
    c.save()
    print(f"Created {filepath}")

policies = [
    {
        "filename": "policy_01_wfh.pdf",
        "title": "Policy 01: Work from Home Policy",
        "content": """
        Effective Date: January 1, 2024
        
        1. Overview
        Practical AI Corp supports flexible work arrangements. This policy outlines the guidelines for working from home (WFH).
        
        2. Eligibility
        All full-time employees are eligible for hybrid work after their first 30 days of employment.
        
        3. Schedule
        - Employees are expected to be in the office at least 3 days a week.
        - Standard remote days are Monday and Friday, unless otherwise requested by the manager.
        - Core collaboration hours are 10:00 AM to 3:00 PM local time. You must be available on Slack and Zoom during these hours.
        
        4. Equipment
        The company provides a laptop and a one-time stipend of $500 for home office setup (monitor, chair, etc.).
        """
    },
    {
        "filename": "policy_02_expenses.pdf",
        "title": "Policy 02: Expense Reimbursement",
        "content": """
        Effective Date: January 1, 2024
        
        1. General Principles
        Expenses must be reasonable, necessary, and business-related.
        
        2. Travel
        - Air Travel: Economy class for domestic flights. Premium Economy for international flights over 8 hours.
        - Lodging: Standard room rate up to $250/night in major cities, $150/night elsewhere.
        
        3. Meals
        - Daily allowance: $75 per day while traveling.
        - Team lunches: $25 per person max.
        - Alcohol: Not reimbursable unless part of a client entertainment event (VP approval required).
        
        4. Submission
        - Receipts are required for all expenses over $25.
        - Expenses must be submitted within 30 days of incurrence via the finance portal.
        """
    },
    {
        "filename": "policy_03_security.pdf",
        "title": "Policy 03: IT Security & Compliance",
        "content": """
        Effective Date: January 1, 2024
        
        1. Password Policy
        - Minimum length: 12 characters.
        - Complexity: Must include uppercase, lowercase, numbers, and symbols.
        - Rotation: Passwords must be changed every 90 days.
        
        2. Multi-Factor Authentication (MFA)
        - MFA is mandatory for all internal systems (Email, GitHub, AWS, HR Portal).
        - Use of an authenticator app (e.g., Google Authenticator, Authy) is preferred over SMS.
        
        3. Device Security
        - Laptops must be encrypted (FileVault/BitLocker).
        - Screen lock must activate after 5 minutes of inactivity.
        - Do not leave devices unattended in public spaces.
        
        4. Data Handling
        - Customer data must never be stored on local machines.
        - Use approved encrypted channels for sharing sensitive credentials.
        """
    }
]

if __name__ == "__main__":
    for policy in policies:
        create_pdf(policy["filename"], policy["title"], policy["content"])

