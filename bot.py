import requests
import json
import time
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class PopMartVip:
    def __init__(self):
        self.base_url = "https://www.popmartvip.cc"
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "www.popmartvip.cc",
            "Origin": self.base_url,
            "Sec-Ch-Ua": '"Chromium";v="130", "Opera";v="116", "Not?A_Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/116.0.0.0 (Edition developer)",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.session.headers.update(self.headers)
        
    def generate_random_email(self):
        """Generate a random email ending with @yopmail.com"""
        username_length = random.randint(8, 15)
        username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(username_length))
        return f"{username}@yopmail.com"
    
    def generate_random_password(self):
        """Generate a random password with uppercase, lowercase, digits and special characters"""
        length = random.randint(10, 14)
        uppercase = random.choice(string.ascii_uppercase)
        lowercase = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice('!@#$%^&*()_+-=')
        
        # Generate the remaining characters
        remaining = ''.join(random.choice(string.ascii_letters + string.digits + '!@#$%^&*()_+-=') 
                           for _ in range(length - 4))
        
        # Combine and shuffle
        password = uppercase + lowercase + digit + special + remaining
        password_list = list(password)
        random.shuffle(password_list)
        return ''.join(password_list)
    
    def get_csrf_token(self):
        """Get CSRF token from the registration page"""
        try:
            response = self.session.get(f"{self.base_url}/login/register")
            # You might need to parse the HTML to extract the CSRF token
            # This is a placeholder - you'll need to adjust based on the actual page structure
            return "AHjHtMzp9Wfx6YgRxmSXZe5nhXKEDXfSADhKZU6U"
        except Exception as e:
            print(f"Error getting CSRF token: {e}")
            return None
    
    def register(self, email, password, invite_code, verification_code):
        """Register a new account"""
        url = f"{self.base_url}/login/register"
        
        # Get CSRF token
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            print("Failed to get CSRF token")
            return False, "CSRF token failure"
        
        # Payload data
        payload = {
            "mobile": email,
            "password": password,
            "inviteCode": invite_code,
            "code": verification_code,
            "_token": csrf_token
        }
        
        # Update headers for this request
        headers = self.headers.copy()
        headers.update({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": f"{self.base_url}/login/register"
        })
        
        try:
            response = self.session.post(url, data=payload, headers=headers)
            result = response.json()
            print(f"Registration Response: {result}")
            
            if result.get("code") == 200:
                print("Registration successful!")
                return True, "Registration successful"
            else:
                error_msg = result.get('msg', 'Unknown error')
                print(f"Registration failed: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error during registration: {e}"
            print(error_msg)
            return False, error_msg
    
    def get_investment_csrf_token(self):
        """Get CSRF token for investment page"""
        try:
            response = self.session.get(f"{self.base_url}/")
            # You might need to parse the HTML to extract the CSRF token
            # This is a placeholder - you'll need to adjust based on the actual page structure
            return "sbsWEbzeMojxxdsYYgwWAghESS4F4SlHMDHDv2Zg"
        except Exception as e:
            print(f"Error getting investment CSRF token: {e}")
            return None
    
    def invest(self, device_id):
        """Make an investment (purchase)"""
        url = f"{self.base_url}/device/invest"
        
        # Get CSRF token
        csrf_token = self.get_investment_csrf_token()
        if not csrf_token:
            print("Failed to get investment CSRF token")
            return False, "CSRF token failure"
        
        # Payload data
        payload = {
            "id": device_id,
            "_token": csrf_token
        }
        
        # Update headers for this request
        headers = self.headers.copy()
        headers.update({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": f"{self.base_url}/"
        })
        
        try:
            response = self.session.post(url, data=payload, headers=headers)
            result = response.json()
            print(f"Investment Response: {result}")
            
            if result.get("code") == 200:
                print("Investment successful!")
                return True, "Investment successful"
            else:
                error_msg = result.get('msg', 'Unknown error')
                print(f"Investment failed: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error during investment: {e}"
            print(error_msg)
            return False, error_msg

class EmailSender:
    def __init__(self, sender_email, sender_password, recipients):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipients = recipients if isinstance(recipients, list) else [recipients]
    
    def send_success_email(self, success_accounts):
        """Send email with successful account details"""
        if not success_accounts:
            print("No successful accounts to report")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ", ".join(self.recipients)
            msg['Subject'] = f"PopMart VIP Success Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            # Create email body
            body = "Successful PopMart VIP Accounts:\n\n"
            for i, account in enumerate(success_accounts, 1):
                body += f"Account {i}:\n"
                body += f"Email: {account['email']}\n"
                body += f"Password: {account['password']}\n"
                body += f"Registration Status: {account['registration_status']}\n"
                body += f"Investment Status: {account['investment_status']}\n"
                body += f"Timestamp: {account['timestamp']}\n"
                body += "-" * 50 + "\n\n"
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipients, msg.as_string())
            
            print("Success email sent successfully!")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

def main():
    # Email configuration
    sender_email = "tajuddeenahmad090@gmail.com"
    sender_password = "jnsh ovzf tdwe jwhc"  # App password for Gmail
    recipients = ["teejeedeeone@gmail.com"]
    
    # Initialize email sender
    email_sender = EmailSender(sender_email, sender_password, recipients)
    
    # Track successful accounts
    successful_accounts = []
    
    # Number of accounts to create
    num_accounts = 1  # You can adjust this number
    
    for i in range(num_accounts):
        print(f"\n=== Creating Account {i+1}/{num_accounts} ===")
        
        # Initialize a new session for each account
        popmart = PopMartVip()
        
        # Generate random credentials
        email = popmart.generate_random_email()
        password = popmart.generate_random_password()
        invite_code = "73fa75d1"
        verification_code = "000000"  # Placeholder - would need real verification in production
        device_id = 3
        
        print(f"Generated Email: {email}")
        print(f"Generated Password: {password}")
        
        # Step 1: Register
        print("Attempting registration...")
        registration_success, registration_msg = popmart.register(email, password, invite_code, verification_code)
        
        account_info = {
            'email': email,
            'password': password,
            'registration_status': registration_msg,
            'investment_status': 'Not attempted',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if registration_success:
            # Add a small delay between registration and investment
            time.sleep(2)
            
            # Step 2: Make investment
            print("Attempting investment...")
            investment_success, investment_msg = popmart.invest(device_id)
            
            account_info['investment_status'] = investment_msg
            
            if investment_success:
                print("Account creation and investment completed successfully!")
                successful_accounts.append(account_info)
            else:
                print("Registration succeeded but investment failed.")
        else:
            print("Registration failed. Investment not attempted.")
        
        # Add delay between account creation attempts to avoid rate limiting
        time.sleep(3)
    
    # Send email with successful accounts
    if successful_accounts:
        print(f"\nSending report for {len(successful_accounts)} successful accounts...")
        email_sender.send_success_email(successful_accounts)
    else:
        print("\nNo successful accounts to report.")

if __name__ == "__main__":
    main()
