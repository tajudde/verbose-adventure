import requests
import json
import time
from datetime import datetime, timezone, timedelta

class EcoXClaimBot:
    def __init__(self):
        self.base_url = "https://api.ecox.network/api/v1"
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlZWplZWRlZW9uZTIwMjZAZ21haWwuY29tIiwic3ViIjoyMDE4MzEsImlhdCI6MTc1NzE5NTY0NSwiZXhwIjoxNzU5Nzg3NjQ1fQ.jc9ux3coHCbRgHK8EM4EQ5Wm4XbowgwL2_0ZB-ZsWFcihw3Scaj8qMob-6qzmQu9FMJumnyFmDGWgkITpvk1yuUK2SVaRaCNcFv5gxMwQzDRxT7gI4XC-f3FHboihJ6tyIWJU-b9A7dkJsw2qdg2HkYmBO8jxRVhNG3nThV103UwaNHV1Te3BI0r0dLAsLewhay8b3rtLco1E8Gny3me96KkAhwlWOL2crWsuLaV-WTKXGcsmB5F666qU0unZg5M5uWtRLP6DBx2uTMB_MJYfk-9lMhsBQXyfKTL7zgfi5mobNYNhIF5Ot3levSaw4Edn0jos9KgniDTv6gAzuFtxQ"
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Authorization": f"Bearer {self.token}",
            "Origin": "https://app.ecox.network",
            "Referer": "https://app.ecox.network/",
        }
    
    def get_stats(self):
        """Get current GREEN stats including claim status"""
        url = f"{self.base_url}/green/stats"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Stats API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Network Error: {e}")
            return None
    
    def make_claim(self):
        """Make a GREEN claim"""
        url = f"{self.base_url}/green/claim"
        
        # For POST request, we need to add proper headers
        claim_headers = self.headers.copy()
        claim_headers["Content-Length"] = "0"
        claim_headers["Content-Type"] = "application/json"
        
        try:
            response = requests.post(url, headers=claim_headers, timeout=10)
            
            print(f"Claim Response Status: {response.status_code}")
            print(f"Claim Response Headers: {dict(response.headers)}")
            
            if response.status_code == 201:
                data = response.json()
                print("✅ Claim successful!")
                return data
            else:
                print(f"❌ Claim API Error: {response.status_code}")
                print(f"❌ Error Response: {response.text}")
                
                # Try to get more details from the error
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        print(f"❌ Error Message: {error_data['error'].get('message', 'Unknown error')}")
                        print(f"❌ Error Path: {error_data['error'].get('path', 'Unknown')}")
                        print(f"❌ Error Timestamp: {error_data['error'].get('timestamp', 'Unknown')}")
                except:
                    pass
                    
                return None
                
        except Exception as e:
            print(f"❌ Network Error during claim: {e}")
            return None
    
    def format_time_remaining(self, seconds):
        """Format time remaining in human-readable format"""
        if seconds <= 0:
            return "READY TO CLAIM NOW!"
        
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        time_parts = []
        if hours > 0:
            time_parts.append(f"{int(hours)}h")
        if minutes > 0:
            time_parts.append(f"{int(minutes)}m")
        if seconds > 0:
            time_parts.append(f"{int(seconds)}s")
        
        return " ".join(time_parts)
    
    def calculate_next_claim_time(self):
        """Calculate when next claim will be available (midnight UTC)"""
        now = datetime.now(timezone.utc)
        
        # Next claim is at midnight UTC
        next_claim_time = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
        return next_claim_time
    
    def check_and_claim(self):
        """Check stats and claim if available"""
        print("🔍 Checking GREEN stats...")
        print("=" * 50)
        
        stats = self.get_stats()
        if not stats:
            return False
        
        data = stats.get("data", {})
        
        # Display current stats
        print(f"💰 Total GREEN: {data.get('totalGreen', 0):.6f}")
        print(f"🎯 Claimable GREEN: {data.get('greenClaimable', 0):.6f}")
        print(f"⚡ Rate per second: {data.get('ratePerSecond', 0):.8f}")
        print(f"🔋 Power Balance: {data.get('powerBalance', 0)}")
        
        can_claim = data.get("canClaim", False)
        last_claim_time = data.get("lastClaimTime")
        
        print(f"✅ Can claim: {'YES!' if can_claim else 'NO'}")
        
        if last_claim_time:
            print(f"⏰ Last claim: {last_claim_time}")
        
        # Calculate next claim time (always midnight UTC)
        next_claim = self.calculate_next_claim_time()
        now = datetime.now(timezone.utc)
        time_remaining = (next_claim - now).total_seconds()
        
        print(f"🔄 Next claim at: {next_claim.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"⏳ Time remaining: {self.format_time_remaining(time_remaining)}")
        
        # If can claim, make the claim!
        if can_claim:
            print("\n🎯 Attempting to claim GREEN...")
            claim_result = self.make_claim()
            
            if claim_result:
                claim_data = claim_result.get("data", {})
                print(f"✅ SUCCESS! Claimed: {claim_data.get('green_amount', 0):.6f} GREEN")
                print(f"💬 {claim_data.get('message', '')}")
                
                # Show next claim time from response
                next_claim_time = claim_data.get("next_claim_time")
                if next_claim_time:
                    print(f"⏰ Next claim available at: {next_claim_time}")
                
                return True
            else:
                print("❌ Claim failed!")
                return False
        else:
            print("\n⏳ Claim not available yet. Waiting for next claim period...")
            return False

def test_authentication():
    """Test the authentication method"""
    print("🧪 Testing Authentication Method...")
    print("=" * 50)
    
    url = "https://api.ecox.network/api/v1/green/stats"
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlZWplZWRlZW9uZTIwMjZAZ21haWwuY29tIiwic3ViIjoyMDE4MzEsImlhdCI6MTc1NzE5NTY0NSwiZXhwIjoxNzU5Nzg3NjQ1fQ.jc9ux3coHCbRgHK8EM4EQ5Wm4XbowgwL2_0ZB-ZsWFcihw3Scaj8qMob-6qzmQu9FMJumnyFmDGWgkITpvk1yuUK2SVaRaCNcFv5gxMwQzDRxT7gI4XC-f3FHboihJ6tyIWJU-b9A7dkJsw2qdg2HkYmBO8jxRVhNG3nThV103UwaNHV1Te3BI0r0dLAsLewhay8b3rtLco1E8Gny3me96KkAhwlWOL2crWsuLaV-WTKXGcsmB5F666qU0unZg5M5uWtRLP6DBx2uTMB_MJYfk-9lMhsBQXyfKTL7zgfi5mobNYNhIF5Ot3levSaw4Edn0jos9KgniDTv6gAzuFtxQ"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print("Status Code:", response.status_code)
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
            data = response.json()
            print(f"Can claim: {data.get('data', {}).get('canClaim', 'Unknown')}")
            print(f"Claimable GREEN: {data.get('data', {}).get('greenClaimable', 0):.6f}")
            return True
        else:
            print("❌ Authentication failed!")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🌿 EcoX GREEN Claim Bot")
    print("=" * 50)
    
    # First test the authentication method
    if not test_authentication():
        print("\n❌ Authentication failed! The token may be invalid or expired.")
        print("💡 Please get a fresh token from your browser session.")
        return
    
    print("\n✅ Authentication successful! Starting bot...")
    
    bot = EcoXClaimBot()
    
    # Run single check
    bot.check_and_claim()

if __name__ == "__main__":
    main()








#####################











#######################


import requests
import json
import time
from datetime import datetime, timezone, timedelta

class EcoXClaimBot:
    def __init__(self):
        self.base_url = "https://api.ecox.network/api/v1"
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlZWplZWRlZW9uZUBnbWFpbC5jb20iLCJzdWIiOjIwMDUxOCwiaWF0IjoxNzU3MjAwNzU1LCJleHAiOjE3NTk3OTI3NTV9.GUqeb78Vn0685BClqaTqPc_QIozJPwAq9W_ORe7ccYbe097XzSiRT00gFiyiRgciAalgkGKfYL3j-gYTFJb9TWqfbe3fRuVQwPuDLSUbAH3suCrWFjZGMyXXeKz19BSYrjHGyNyAj8oOV65_TMH1fTfslPx5gNdcGRAWV97jE8lZ60U8B8StAROMhrWcEqDeTKCwcsuTKV1AMec8OLGlstL9JBjL_8LdUuZVL2tCscjgVM97p96P0aZfUjzii98HIYZ16brTtKiuueKbFwiI3PDwuyzNdyGkmKJr92zm7wvU_J2iIIbrVZiLiXMkGnKc-WIxX6lF1bGOWP1sg2dHzg"
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Authorization": f"Bearer {self.token}",
            "Origin": "https://app.ecox.network",
            "Referer": "https://app.ecox.network/",
        }
    
    def get_stats(self):
        """Get current GREEN stats including claim status"""
        url = f"{self.base_url}/green/stats"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Stats API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Network Error: {e}")
            return None
    
    def make_claim(self):
        """Make a GREEN claim"""
        url = f"{self.base_url}/green/claim"
        
        # For POST request, we need to add proper headers
        claim_headers = self.headers.copy()
        claim_headers["Content-Length"] = "0"
        claim_headers["Content-Type"] = "application/json"
        
        try:
            response = requests.post(url, headers=claim_headers, timeout=10)
            
            print(f"Claim Response Status: {response.status_code}")
            print(f"Claim Response Headers: {dict(response.headers)}")
            
            if response.status_code == 201:
                data = response.json()
                print("✅ Claim successful!")
                return data
            else:
                print(f"❌ Claim API Error: {response.status_code}")
                print(f"❌ Error Response: {response.text}")
                
                # Try to get more details from the error
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        print(f"❌ Error Message: {error_data['error'].get('message', 'Unknown error')}")
                        print(f"❌ Error Path: {error_data['error'].get('path', 'Unknown')}")
                        print(f"❌ Error Timestamp: {error_data['error'].get('timestamp', 'Unknown')}")
                except:
                    pass
                    
                return None
                
        except Exception as e:
            print(f"❌ Network Error during claim: {e}")
            return None
    
    def format_time_remaining(self, seconds):
        """Format time remaining in human-readable format"""
        if seconds <= 0:
            return "READY TO CLAIM NOW!"
        
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        time_parts = []
        if hours > 0:
            time_parts.append(f"{int(hours)}h")
        if minutes > 0:
            time_parts.append(f"{int(minutes)}m")
        if seconds > 0:
            time_parts.append(f"{int(seconds)}s")
        
        return " ".join(time_parts)
    
    def calculate_next_claim_time(self):
        """Calculate when next claim will be available (midnight UTC)"""
        now = datetime.now(timezone.utc)
        
        # Next claim is at midnight UTC
        next_claim_time = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
        return next_claim_time
    
    def check_and_claim(self):
        """Check stats and claim if available"""
        print("🔍 Checking GREEN stats...")
        print("=" * 50)
        
        stats = self.get_stats()
        if not stats:
            return False
        
        data = stats.get("data", {})
        
        # Display current stats
        print(f"💰 Total GREEN: {data.get('totalGreen', 0):.6f}")
        print(f"🎯 Claimable GREEN: {data.get('greenClaimable', 0):.6f}")
        print(f"⚡ Rate per second: {data.get('ratePerSecond', 0):.8f}")
        print(f"🔋 Power Balance: {data.get('powerBalance', 0)}")
        
        can_claim = data.get("canClaim", False)
        last_claim_time = data.get("lastClaimTime")
        
        print(f"✅ Can claim: {'YES!' if can_claim else 'NO'}")
        
        if last_claim_time:
            print(f"⏰ Last claim: {last_claim_time}")
        
        # Calculate next claim time (always midnight UTC)
        next_claim = self.calculate_next_claim_time()
        now = datetime.now(timezone.utc)
        time_remaining = (next_claim - now).total_seconds()
        
        print(f"🔄 Next claim at: {next_claim.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"⏳ Time remaining: {self.format_time_remaining(time_remaining)}")
        
        # If can claim, make the claim!
        if can_claim:
            print("\n🎯 Attempting to claim GREEN...")
            claim_result = self.make_claim()
            
            if claim_result:
                claim_data = claim_result.get("data", {})
                print(f"✅ SUCCESS! Claimed: {claim_data.get('green_amount', 0):.6f} GREEN")
                print(f"💬 {claim_data.get('message', '')}")
                
                # Show next claim time from response
                next_claim_time = claim_data.get("next_claim_time")
                if next_claim_time:
                    print(f"⏰ Next claim available at: {next_claim_time}")
                
                return True
            else:
                print("❌ Claim failed!")
                return False
        else:
            print("\n⏳ Claim not available yet. Waiting for next claim period...")
            return False

def test_authentication():
    """Test the authentication method"""
    print("🧪 Testing Authentication Method...")
    print("=" * 50)
    
    url = "https://api.ecox.network/api/v1/green/stats"
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlZWplZWRlZW9uZUBnbWFpbC5jb20iLCJzdWIiOjIwMDUxOCwiaWF0IjoxNzU3MjAwNzU1LCJleHAiOjE3NTk3OTI3NTV9.GUqeb78Vn0685BClqaTqPc_QIozJPwAq9W_ORe7ccYbe097XzSiRT00gFiyiRgciAalgkGKfYL3j-gYTFJb9TWqfbe3fRuVQwPuDLSUbAH3suCrWFjZGMyXXeKz19BSYrjHGyNyAj8oOV65_TMH1fTfslPx5gNdcGRAWV97jE8lZ60U8B8StAROMhrWcEqDeTKCwcsuTKV1AMec8OLGlstL9JBjL_8LdUuZVL2tCscjgVM97p96P0aZfUjzii98HIYZ16brTtKiuueKbFwiI3PDwuyzNdyGkmKJr92zm7wvU_J2iIIbrVZiLiXMkGnKc-WIxX6lF1bGOWP1sg2dHzg"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print("Status Code:", response.status_code)
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
            data = response.json()
            print(f"Can claim: {data.get('data', {}).get('canClaim', 'Unknown')}")
            print(f"Claimable GREEN: {data.get('data', {}).get('greenClaimable', 0):.6f}")
            return True
        else:
            print("❌ Authentication failed!")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🌿 EcoX GREEN Claim Bot")
    print("=" * 50)
    
    # First test the authentication method
    if not test_authentication():
        print("\n❌ Authentication failed! The token may be invalid or expired.")
        print("💡 Please get a fresh token from your browser session.")
        return
    
    print("\n✅ Authentication successful! Starting bot...")
    
    bot = EcoXClaimBot()
    
    # Run single check
    bot.check_and_claim()

if __name__ == "__main__":
    main()






#####################################


###########

import requests
import json
import time
from datetime import datetime, timezone, timedelta

class EcoXClaimBot:
    def __init__(self):
        self.base_url = "https://api.ecox.network/api/v1"
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlZWplZWRlZW9uZTIwMjVAZ21haWwuY29tIiwic3ViIjoyMDE3MzEsImlhdCI6MTc1NzIwMDkxOCwiZXhwIjoxNzU5NzkyOTE4fQ.opTjvGTAqCfV9P-VpKAGOogdN4ihoxzkDzCaQst3Cv0SSoPfmxE3zkEYC5Vpq4HPiOXZw05YYZugJtv5Aj842uVkpnL__Pzn5anDEZZex3PWrWa6KcSmb2drVJ8xDXMWE4qu9LKiHPLoesKuokNu97HfWETNDrou2Vhf9n3PHSeRt__Rz2gk-JESf4yhV-xzLFPjfKcSBNbfsjzVfg2hz9Mj7P0IsUe4cEAXatooGhGcH_0CDb0vf9H2qdDUfkX-I2bic-tyrKkCeN5iej1IIJ17BXGd0VakibAVw1DEnsOBsUk41p2-5spuyMdkXR4_shoOzNmSU-TpOICGePCICQ"
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Authorization": f"Bearer {self.token}",
            "Origin": "https://app.ecox.network",
            "Referer": "https://app.ecox.network/",
        }
    
    def get_stats(self):
        """Get current GREEN stats including claim status"""
        url = f"{self.base_url}/green/stats"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Stats API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Network Error: {e}")
            return None
    
    def make_claim(self):
        """Make a GREEN claim"""
        url = f"{self.base_url}/green/claim"
        
        # For POST request, we need to add proper headers
        claim_headers = self.headers.copy()
        claim_headers["Content-Length"] = "0"
        claim_headers["Content-Type"] = "application/json"
        
        try:
            response = requests.post(url, headers=claim_headers, timeout=10)
            
            print(f"Claim Response Status: {response.status_code}")
            print(f"Claim Response Headers: {dict(response.headers)}")
            
            if response.status_code == 201:
                data = response.json()
                print("✅ Claim successful!")
                return data
            else:
                print(f"❌ Claim API Error: {response.status_code}")
                print(f"❌ Error Response: {response.text}")
                
                # Try to get more details from the error
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        print(f"❌ Error Message: {error_data['error'].get('message', 'Unknown error')}")
                        print(f"❌ Error Path: {error_data['error'].get('path', 'Unknown')}")
                        print(f"❌ Error Timestamp: {error_data['error'].get('timestamp', 'Unknown')}")
                except:
                    pass
                    
                return None
                
        except Exception as e:
            print(f"❌ Network Error during claim: {e}")
            return None
    
    def format_time_remaining(self, seconds):
        """Format time remaining in human-readable format"""
        if seconds <= 0:
            return "READY TO CLAIM NOW!"
        
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        time_parts = []
        if hours > 0:
            time_parts.append(f"{int(hours)}h")
        if minutes > 0:
            time_parts.append(f"{int(minutes)}m")
        if seconds > 0:
            time_parts.append(f"{int(seconds)}s")
        
        return " ".join(time_parts)
    
    def calculate_next_claim_time(self):
        """Calculate when next claim will be available (midnight UTC)"""
        now = datetime.now(timezone.utc)
        
        # Next claim is at midnight UTC
        next_claim_time = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
        return next_claim_time
    
    def check_and_claim(self):
        """Check stats and claim if available"""
        print("🔍 Checking GREEN stats...")
        print("=" * 50)
        
        stats = self.get_stats()
        if not stats:
            return False
        
        data = stats.get("data", {})
        
        # Display current stats
        print(f"💰 Total GREEN: {data.get('totalGreen', 0):.6f}")
        print(f"🎯 Claimable GREEN: {data.get('greenClaimable', 0):.6f}")
        print(f"⚡ Rate per second: {data.get('ratePerSecond', 0):.8f}")
        print(f"🔋 Power Balance: {data.get('powerBalance', 0)}")
        
        can_claim = data.get("canClaim", False)
        last_claim_time = data.get("lastClaimTime")
        
        print(f"✅ Can claim: {'YES!' if can_claim else 'NO'}")
        
        if last_claim_time:
            print(f"⏰ Last claim: {last_claim_time}")
        
        # Calculate next claim time (always midnight UTC)
        next_claim = self.calculate_next_claim_time()
        now = datetime.now(timezone.utc)
        time_remaining = (next_claim - now).total_seconds()
        
        print(f"🔄 Next claim at: {next_claim.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"⏳ Time remaining: {self.format_time_remaining(time_remaining)}")
        
        # If can claim, make the claim!
        if can_claim:
            print("\n🎯 Attempting to claim GREEN...")
            claim_result = self.make_claim()
            
            if claim_result:
                claim_data = claim_result.get("data", {})
                print(f"✅ SUCCESS! Claimed: {claim_data.get('green_amount', 0):.6f} GREEN")
                print(f"💬 {claim_data.get('message', '')}")
                
                # Show next claim time from response
                next_claim_time = claim_data.get("next_claim_time")
                if next_claim_time:
                    print(f"⏰ Next claim available at: {next_claim_time}")
                
                return True
            else:
                print("❌ Claim failed!")
                return False
        else:
            print("\n⏳ Claim not available yet. Waiting for next claim period...")
            return False

def test_authentication():
    """Test the authentication method"""
    print("🧪 Testing Authentication Method...")
    print("=" * 50)
    
    url = "https://api.ecox.network/api/v1/green/stats"
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlZWplZWRlZW9uZTIwMjVAZ21haWwuY29tIiwic3ViIjoyMDE3MzEsImlhdCI6MTc1NzIwMDkxOCwiZXhwIjoxNzU5NzkyOTE4fQ.opTjvGTAqCfV9P-VpKAGOogdN4ihoxzkDzCaQst3Cv0SSoPfmxE3zkEYC5Vpq4HPiOXZw05YYZugJtv5Aj842uVkpnL__Pzn5anDEZZex3PWrWa6KcSmb2drVJ8xDXMWE4qu9LKiHPLoesKuokNu97HfWETNDrou2Vhf9n3PHSeRt__Rz2gk-JESf4yhV-xzLFPjfKcSBNbfsjzVfg2hz9Mj7P0IsUe4cEAXatooGhGcH_0CDb0vf9H2qdDUfkX-I2bic-tyrKkCeN5iej1IIJ17BXGd0VakibAVw1DEnsOBsUk41p2-5spuyMdkXR4_shoOzNmSU-TpOICGePCICQ"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print("Status Code:", response.status_code)
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
            data = response.json()
            print(f"Can claim: {data.get('data', {}).get('canClaim', 'Unknown')}")
            print(f"Claimable GREEN: {data.get('data', {}).get('greenClaimable', 0):.6f}")
            return True
        else:
            print("❌ Authentication failed!")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🌿 EcoX GREEN Claim Bot")
    print("=" * 50)
    
    # First test the authentication method
    if not test_authentication():
        print("\n❌ Authentication failed! The token may be invalid or expired.")
        print("💡 Please get a fresh token from your browser session.")
        return
    
    print("\n✅ Authentication successful! Starting bot...")
    
    bot = EcoXClaimBot()
    
    # Run single check
    bot.check_and_claim()

if __name__ == "__main__":
    main()






##################

import requests
import json
import time
from datetime import datetime, timezone, timedelta

class EcoXClaimBot:
    def __init__(self):
        self.base_url = "https://api.ecox.network/api/v1"
        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRhanVkZGVlbmFobWFkMDkwQGdtYWlsLmNvbSIsInN1YiI6MTg3NzI4LCJpYXQiOjE3NTcyMDEyMzcsImV4cCI6MTc1OTc5MzIzN30.cUp75mAeHcNZemmHLGdV1QWkyNyX0MLO7NcxKj7DZux1h26eA6--ifyhBLujgbToI1lDXwxac--aGcWlhaiSUi63dS2uovX-a3-IjOZrXIJBovj725r34wmvfBvlx723LqWmBaDHU6rjEnuOO7FFNmS8SOrkxrk6kSroijhTmGWoVmo-esFEU9-n7ZYIOgEEbHrokWnCC7rxYBXaDE6tAXWvRCwqphV046yPf5mSbZGbyElHgoY_zVG99xtD7V2Gx8TUbXao43lAY3xCftN8h2uuifJsliIfPCz3s-6iCJP9SbtJtGY_HCHOh993CQKndOLFTlF5SEwIz5XLzHzzdA"
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Authorization": f"Bearer {self.token}",
            "Origin": "https://app.ecox.network",
            "Referer": "https://app.ecox.network/",
        }
    
    def get_stats(self):
        """Get current GREEN stats including claim status"""
        url = f"{self.base_url}/green/stats"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Stats API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Network Error: {e}")
            return None
    
    def make_claim(self):
        """Make a GREEN claim"""
        url = f"{self.base_url}/green/claim"
        
        # For POST request, we need to add proper headers
        claim_headers = self.headers.copy()
        claim_headers["Content-Length"] = "0"
        claim_headers["Content-Type"] = "application/json"
        
        try:
            response = requests.post(url, headers=claim_headers, timeout=10)
            
            print(f"Claim Response Status: {response.status_code}")
            print(f"Claim Response Headers: {dict(response.headers)}")
            
            if response.status_code == 201:
                data = response.json()
                print("✅ Claim successful!")
                return data
            else:
                print(f"❌ Claim API Error: {response.status_code}")
                print(f"❌ Error Response: {response.text}")
                
                # Try to get more details from the error
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        print(f"❌ Error Message: {error_data['error'].get('message', 'Unknown error')}")
                        print(f"❌ Error Path: {error_data['error'].get('path', 'Unknown')}")
                        print(f"❌ Error Timestamp: {error_data['error'].get('timestamp', 'Unknown')}")
                except:
                    pass
                    
                return None
                
        except Exception as e:
            print(f"❌ Network Error during claim: {e}")
            return None
    
    def format_time_remaining(self, seconds):
        """Format time remaining in human-readable format"""
        if seconds <= 0:
            return "READY TO CLAIM NOW!"
        
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        time_parts = []
        if hours > 0:
            time_parts.append(f"{int(hours)}h")
        if minutes > 0:
            time_parts.append(f"{int(minutes)}m")
        if seconds > 0:
            time_parts.append(f"{int(seconds)}s")
        
        return " ".join(time_parts)
    
    def calculate_next_claim_time(self):
        """Calculate when next claim will be available (midnight UTC)"""
        now = datetime.now(timezone.utc)
        
        # Next claim is at midnight UTC
        next_claim_time = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
        return next_claim_time
    
    def check_and_claim(self):
        """Check stats and claim if available"""
        print("🔍 Checking GREEN stats...")
        print("=" * 50)
        
        stats = self.get_stats()
        if not stats:
            return False
        
        data = stats.get("data", {})
        
        # Display current stats
        print(f"💰 Total GREEN: {data.get('totalGreen', 0):.6f}")
        print(f"🎯 Claimable GREEN: {data.get('greenClaimable', 0):.6f}")
        print(f"⚡ Rate per second: {data.get('ratePerSecond', 0):.8f}")
        print(f"🔋 Power Balance: {data.get('powerBalance', 0)}")
        
        can_claim = data.get("canClaim", False)
        last_claim_time = data.get("lastClaimTime")
        
        print(f"✅ Can claim: {'YES!' if can_claim else 'NO'}")
        
        if last_claim_time:
            print(f"⏰ Last claim: {last_claim_time}")
        
        # Calculate next claim time (always midnight UTC)
        next_claim = self.calculate_next_claim_time()
        now = datetime.now(timezone.utc)
        time_remaining = (next_claim - now).total_seconds()
        
        print(f"🔄 Next claim at: {next_claim.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"⏳ Time remaining: {self.format_time_remaining(time_remaining)}")
        
        # If can claim, make the claim!
        if can_claim:
            print("\n🎯 Attempting to claim GREEN...")
            claim_result = self.make_claim()
            
            if claim_result:
                claim_data = claim_result.get("data", {})
                print(f"✅ SUCCESS! Claimed: {claim_data.get('green_amount', 0):.6f} GREEN")
                print(f"💬 {claim_data.get('message', '')}")
                
                # Show next claim time from response
                next_claim_time = claim_data.get("next_claim_time")
                if next_claim_time:
                    print(f"⏰ Next claim available at: {next_claim_time}")
                
                return True
            else:
                print("❌ Claim failed!")
                return False
        else:
            print("\n⏳ Claim not available yet. Waiting for next claim period...")
            return False

def test_authentication():
    """Test the authentication method"""
    print("🧪 Testing Authentication Method...")
    print("=" * 50)
    
    url = "https://api.ecox.network/api/v1/green/stats"
    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRhanVkZGVlbmFobWFkMDkwQGdtYWlsLmNvbSIsInN1YiI6MTg3NzI4LCJpYXQiOjE3NTcyMDEyMzcsImV4cCI6MTc1OTc5MzIzN30.cUp75mAeHcNZemmHLGdV1QWkyNyX0MLO7NcxKj7DZux1h26eA6--ifyhBLujgbToI1lDXwxac--aGcWlhaiSUi63dS2uovX-a3-IjOZrXIJBovj725r34wmvfBvlx723LqWmBaDHU6rjEnuOO7FFNmS8SOrkxrk6kSroijhTmGWoVmo-esFEU9-n7ZYIOgEEbHrokWnCC7rxYBXaDE6tAXWvRCwqphV046yPf5mSbZGbyElHgoY_zVG99xtD7V2Gx8TUbXao43lAY3xCftN8h2uuifJsliIfPCz3s-6iCJP9SbtJtGY_HCHOh993CQKndOLFTlF5SEwIz5XLzHzzdA"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print("Status Code:", response.status_code)
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
            data = response.json()
            print(f"Can claim: {data.get('data', {}).get('canClaim', 'Unknown')}")
            print(f"Claimable GREEN: {data.get('data', {}).get('greenClaimable', 0):.6f}")
            return True
        else:
            print("❌ Authentication failed!")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🌿 EcoX GREEN Claim Bot")
    print("=" * 50)
    
    # First test the authentication method
    if not test_authentication():
        print("\n❌ Authentication failed! The token may be invalid or expired.")
        print("💡 Please get a fresh token from your browser session.")
        return
    
    print("\n✅ Authentication successful! Starting bot...")
    
    bot = EcoXClaimBot()
    
    # Run single check
    bot.check_and_claim()

if __name__ == "__main__":
    main()
