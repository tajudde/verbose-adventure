import requests
import json
import time
from datetime import datetime, timezone, timedelta

class EcoXClaimBot:
    def __init__(self, tokens):
        self.base_url = "https://api.ecox.network/api/v1"
        self.tokens = tokens
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Origin": "https://app.ecox.network",
            "Referer": "https://app.ecox.network/",
        }
    
    def get_stats(self, token):
        """Get current GREEN stats including claim status"""
        url = f"{self.base_url}/green/stats"
        
        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {token}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Stats API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Network Error: {e}")
            return None
    
    def make_claim(self, token):
        """Make a GREEN claim"""
        url = f"{self.base_url}/green/claim"
        
        # For POST request, we need to add proper headers
        claim_headers = self.headers.copy()
        claim_headers["Authorization"] = f"Bearer {token}"
        claim_headers["Content-Length"] = "0"
        claim_headers["Content-Type"] = "application/json"
        
        try:
            response = requests.post(url, headers=claim_headers, timeout=10)
            
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
                except:
                    pass
                    
                return None
                
        except Exception as e:
            print(f"❌ Network Error during claim: {e}")
            return None
    
    def process_account(self, token, account_num):
        """Process a single account"""
        print(f"\n{'='*60}")
        print(f"👤 Processing Account #{account_num}")
        print(f"{'='*60}")
        
        # Get stats first
        stats = self.get_stats(token)
        if not stats:
            print("❌ Failed to get stats for this account")
            return False
        
        data = stats.get("data", {})
        
        # Display current stats
        print(f"💰 Total GREEN: {data.get('totalGreen', 0):.6f}")
        print(f"🎯 Claimable GREEN: {data.get('greenClaimable', 0):.6f}")
        print(f"⚡ Rate per second: {data.get('ratePerSecond', 0):.8f}")
        print(f"🔋 Power Balance: {data.get('powerBalance', 0)}")
        
        last_claim_time = data.get("lastClaimTime")
        if last_claim_time:
            print(f"⏰ Last claim: {last_claim_time}")
        
        # Always attempt to claim regardless of status
        print("\n🎯 Attempting to claim GREEN...")
        claim_result = self.make_claim(token)
        
        if claim_result:
            claim_data = claim_result.get("data", {})
            print(f"✅ SUCCESS! Claimed: {claim_data.get('green_amount', 0):.6f} GREEN")
            print(f"💬 {claim_data.get('message', '')}")
            return True
        else:
            print("❌ Claim failed!")
            return False
    
    def process_all_accounts(self):
        """Process all accounts in sequence"""
        print("🌿 EcoX GREEN Claim Bot - Multiple Accounts")
        print("=" * 60)
        
        successful_claims = 0
        total_accounts = len(self.tokens)
        
        for i, token in enumerate(self.tokens, 1):
            print(f"\n📊 Processing account {i} of {total_accounts}")
            if self.process_account(token, i):
                successful_claims += 1
            
            # Add a small delay between accounts to avoid rate limiting
            if i < total_accounts:
                print("\n⏳ Waiting 2 seconds before next account...")
                time.sleep(2)
        
        print(f"\n{'='*60}")
        print(f"📈 Summary: {successful_claims} of {total_accounts} accounts claimed successfully")
        print(f"{'='*60}")

def main():
    """Main function"""
    # Add all your tokens here
    tokens = [
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlZWplZWRlZW9uZTIwMjZAZ21haWwuY29tIiwic3ViIjoyMDE4MzEsImlhdCI6MTc1NzE5NTY0NSwiZXhwIjoxNzU5Nzg3NjQ1fQ.jc9ux3coHCbRgHK8EM4EQ5Wm4XbowgwL2_0ZB-ZsWFcihw3Scaj8qMob-6qzmQu9FMJumnyFmDGWgkITpvk1yuUK2SVaRaCNcFv5gxMwQzDRxT7gI4XC-f3FHboihJ6tyIWJU-b9A7dkJsw2qdg2HkYmBO8jxRVhNG3nThV103UwaNHV1Te3BI0r0dLAsLewhay8b3rtLco1E8Gny3me96KkAhwlWOL2crWsuLaV-WTKXGcsmB5F666qU0unZg5M5uWtRLP6DBx2uTMB_MJYfk-9lMhsBQXyfKTL7zgfi5mobNYNhIF5Ot3levSaw4Edn0jos9KgniDTv6gAzuFtxQ",
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlZWplZWRlZW9uZUBnbWFpbC5jb20iLCJzdWIiOjIwMDUxOCwiaWF0IjoxNzU3MjAwNzU1LCJleHAiOjE3NTk3OTI3NTV9.GUqeb78Vn0685BClqaTqPc_QIozJPwAq9W_ORe7ccYbe097XzSiRT00gFiyiRgciAalgkGKfYL3j-gYTFJb9TWqfbe3fRuVQwPuDLSUbAH3suCrWFjZGMyXXeKz19BSYrjHGyNyAj8oOV65_TMH1fTfslPx5gNdcGRAWV97jE8lZ60U8B8StAROMhrWcEqDeTKCwcsuTKV1AMec8OLGlstL9JBjL_8LdUuZVL2tCscjgVM97p96P0aZfUjzii98HIYZ16brTtKiuueKbFwiI3PDwuyzNdyGkmKJr92zm7wvU_J2iIIbrVZiLiXMkGnKc-WIxX6lF1bGOWP1sg2dHzg",
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlZWplZWRlZW9uZTIwMjVAZ21haWwuY29tIiwic3ViIjoyMDE3MzEsImlhdCI6MTc1NzIwMDkxOCwiZXhwIjoxNzU5NzkyOTE4fQ.opTjvGTAqCfV9P-VpKAGOogdN4ihoxzkDzCaQst3Cv0SSoPfmxE3zkEYC5Vpq4HPiOXZw05YYZugJtv5Aj842uVkpnL__Pzn5anDEZZex3PWrWa6KcSmb2drVJ8xDXMWE4qu9LKiHPLoesKuokNu97HfWETNDrou2Vhf9n3PHSeRt__Rz2gk-JESf4yhV-xzLFPjfKcSBNbfsjzVfg2hz9Mj7P0IsUe4cEAXatooGhGcH_0CDb0vf9H2qdDUfkX-I2bic-tyrKkCeN5iej1IIJ17BXGd0VakibAVw1DEnsOBsUk41p2-5spuyMdkXR4_shoOzNmSU-TpOICGePCICQ",
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRhanVkZGVlbmFobWFkMDkwQGdtYWlsLmNvbSIsInN1YiI6MTg3NzI4LCJpYXQiOjE3NTcyMDEyMzcsImV4cCI6MTc1OTc5MzIzN30.cUp75mAeHcNZemmHLGdV1QWkyNyX0MLO7NcxKj7DZux1h26eA6--ifyhBLujgbToI1lDXwxac--aGcWlhaiSUi63dS2uovX-a3-IjOZrXIJBovj725r34wmvfBvlx723LqWmBaDHU6rjEnuOO7FFNmS8SOrkxrk6kSroijhTmGWoVmo-esFEU9-n7ZYIOgEEbHrokWnCC7rxYBXaDE6tAXWvRCwqphV046yPf5mSbZGbyElHgoY_zVG99xtD7V2Gx8TUbXao43lAY3xCftN8h2uuifJsliIfPCz3s-6iCJP9SbtJtGY_HCHOh993CQKndOLFTlF5SEwIz5XLzHzzdA"
    ]
    
    # Initialize bot with all tokens
    bot = EcoXClaimBot(tokens)
    
    # Process all accounts
    bot.process_all_accounts()

if __name__ == "__main__":
    main()
