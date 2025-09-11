import requests
import time
import json
import random
import os
import gzip
import io
from datetime import datetime, timedelta
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

class EcoXBot:
    def __init__(self, bearer_token):
        self.base_url = "https://api.ecox.network/api/v1"
        
        # Rotating user agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ]
        
        self.headers = {
            "authorization": f"Bearer {bearer_token}",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",  # Keep this but handle decompression
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://app.ecox.network",
            "priority": "u=1, i",
            "referer": "https://app.ecox.network/",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "content-type": "application/json"
        }
        
        self.comments = [
            "Great post! 👍",
            "Awesome work! 🌱",
            "Keep up the good work! 💚",
            "Amazing environmental effort! 🌍",
            "Love this initiative! ♻️",
            "Fantastic contribution to sustainability! 🌿",
            "Well done! 👏",
            "Inspiring content! ✨",
            "This is wonderful! 🌟",
            "Excellent eco-action! 🍃"
        ]

    def decompress_response(self, response):
        """Handle gzip/deflate compressed responses"""
        if response.headers.get('Content-Encoding') == 'gzip':
            try:
                compressed_data = io.BytesIO(response.content)
                with gzip.GzipFile(fileobj=compressed_data) as f:
                    return f.read().decode('utf-8')
            except Exception as e:
                print(f"❌ Gzip decompression error: {e}")
                return response.text
        else:
            return response.text

    def get_community_articles(self):
        """Fetch community articles"""
        url = f"{self.base_url}/community/list-article"
        cache_bust = int(time.time() * 1000)
        params = {
            "limit": 10,
            "offset": 1,
            "_cacheBust": cache_bust
        }

        # Use a simpler approach without IP spoofing
        current_headers = self.headers.copy()
        current_headers["user-agent"] = random.choice(self.user_agents)

        try:
            response = requests.get(
                url, 
                params=params, 
                headers=current_headers, 
                timeout=15,
                verify=False
            )
            
            print(f"🔍 API Response Status: {response.status_code}")
            print(f"🔍 Content-Encoding: {response.headers.get('Content-Encoding')}")
            
            # Handle compressed response
            response_text = self.decompress_response(response)
            print(f"🔍 Decompressed Length: {len(response_text)} characters")
            
            if response.status_code == 200:
                try:
                    # Try to parse as JSON
                    data = json.loads(response_text)
                    return data
                except json.JSONDecodeError:
                    print(f"❌ JSON decode error. First 100 chars: {response_text[:100]}")
                    return None
            else:
                print(f"❌ API returned status {response.status_code}")
                print(f"❌ Response: {response_text[:200]}...")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Connection error")
            return None
        except Exception as e:
            print(f"❌ Error fetching articles: {e}")
            return None

    def make_api_request(self, method, url, **kwargs):
        """Generic API request method with compression handling"""
        try:
            response = requests.request(
                method, 
                url, 
                timeout=10,
                verify=False,
                **kwargs
            )
            
            # Handle compressed response
            response_text = self.decompress_response(response)
            
            if response.status_code in [200, 201]:
                try:
                    return json.loads(response_text) if response_text else True
                except json.JSONDecodeError:
                    return True  # For actions that don't return JSON
            else:
                print(f"❌ API error {response.status_code}: {response_text[:100]}")
                return False
                
        except Exception as e:
            print(f"❌ API request error: {e}")
            return False

    def like_article(self, slug):
        """Like an article"""
        if random.random() < 0.1:
            print("⏭️  Skipping like (random skip)")
            return False

        url = f"{self.base_url}/community/article-like"
        payload = {"slug": slug}

        try:
            time.sleep(random.uniform(1, 2))
            result = self.make_api_request('POST', url, json=payload, headers=self.headers)
            if result:
                print(f"✅ Liked article: {slug}")
                return True
            else:
                print(f"❌ Failed to like article: {slug}")
                return False
        except Exception as e:
            print(f"❌ Error liking article: {e}")
            return False

    def comment_on_article(self, slug):
        """Comment on an article"""
        url = f"{self.base_url}/community/article-comment"
        comment = random.choice(self.comments)
        payload = {
            "slug": slug,
            "content": comment
        }

        try:
            time.sleep(random.uniform(1.5, 2.5))
            result = self.make_api_request('POST', url, json=payload, headers=self.headers)
            if result:
                print(f"💬 Commented on article: {comment}")
                return True
            else:
                print(f"❌ Failed to comment on article: {slug}")
                return False
        except Exception as e:
            print(f"❌ Error commenting on article: {e}")
            return False

    def visit_user_profile(self, username):
        """Visit user profile"""
        if random.random() < 0.1:
            print("⏭️  Skipping profile visit (random skip)")
            return None

        url = f"{self.base_url}/community/stat"
        params = {"username": username}

        try:
            time.sleep(random.uniform(1, 1.5))
            result = self.make_api_request('GET', url, params=params, headers=self.headers)
            if result and 'data' in result:
                print(f"👤 Visited profile: {username} - {result['data']['name']}")
                return result
            else:
                print(f"❌ Failed to visit profile: {username}")
                return None
        except Exception as e:
            print(f"❌ Error visiting profile: {e}")
            return None

    def follow_user(self, uid):
        """Follow a user"""
        if random.random() < 0.1:
            print("⏭️  Skipping follow (random skip)")
            return False

        url = f"{self.base_url}/user/follow"
        payload = {"uid": uid}

        try:
            time.sleep(random.uniform(1, 1.5))
            result = self.make_api_request('POST', url, json=payload, headers=self.headers)
            if result:
                print(f"🤝 Followed user: {uid}")
                return True
            else:
                print(f"❌ Failed to follow user: {uid}")
                return False
        except Exception as e:
            print(f"❌ Error following user: {e}")
            return False

    def run_bot(self, duration_minutes=2):
        """Run the bot for specified duration"""
        print(f"🤖 Starting EcoX Bot for {duration_minutes} minutes...")
        print(f"🌐 Environment: {'GitHub Actions' if 'GITHUB_ACTIONS' in os.environ else 'Local/Colab'}")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)

        actions_performed = {
            'articles_fetched': 0,
            'likes': 0,
            'comments': 0,
            'profiles_visited': 0,
            'follows': 0
        }

        successful_cycles = 0
        
        while time.time() < end_time and successful_cycles < 5:  # Limit cycles for testing
            print(f"\n🔄 Cycle started at {datetime.now().strftime('%H:%M:%S')}")

            # Fetch articles
            articles_data = self.get_community_articles()
            if not articles_data or 'data' not in articles_data:
                print("❌ No articles found or error fetching articles")
                time.sleep(random.uniform(3, 5))
                continue

            actions_performed['articles_fetched'] += 1
            articles = articles_data['data']
            successful_cycles += 1

            print(f"📰 Found {len(articles)} articles")

            # Process each article with random selection
            processed_articles = random.sample(articles, min(2, len(articles)))

            for article in processed_articles:
                slug = article['slug']
                username = article['user']['username']

                print(f"\n📝 Processing article: {slug[:10]}... by {username}")

                # Like article
                if self.like_article(slug):
                    actions_performed['likes'] += 1

                # Comment on article
                if self.comment_on_article(slug):
                    actions_performed['comments'] += 1

                # Visit user profile
                user_data = self.visit_user_profile(username)
                if user_data:
                    actions_performed['profiles_visited'] += 1

                    # Follow user
                    if self.follow_user(username):
                        actions_performed['follows'] += 1

                time.sleep(random.uniform(2, 3))

            cycle_delay = random.uniform(5, 8)
            print(f"⏳ Waiting {cycle_delay:.1f} seconds before next cycle...")
            time.sleep(cycle_delay)

            elapsed = time.time() - start_time
            remaining = end_time - time.time()
            print(f"⏰ Elapsed: {elapsed:.0f}s, Remaining: {remaining:.0f}s")

        print(f"\n🎯 Bot session completed!")
        print(f"📊 Summary:")
        print(f"   Articles fetched: {actions_performed['articles_fetched']}")
        print(f"   Likes: {actions_performed['likes']}")
        print(f"   Comments: {actions_performed['comments']}")
        print(f"   Profiles visited: {actions_performed['profiles_visited']}")
        print(f"   Follows: {actions_performed['follows']}")

def main():
    bearer_token = os.getenv('ECOX_BEARER_TOKEN')

    if not bearer_token:
        bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRhaG1hZHUwNzFAZ21haWwuY29tIiwic3ViIjoxNzI5MTUsImlhdCI6MTc1NzYxMzgwNywiZXhwIjoxNzYwMjA1ODA3fQ.beemPqIyWocCE5PGh_zpRhSF2OIUHJ4avAuLQSdoq0fzIB-gypfBT_jaUgEps9vI10_HtbY3HqeLqpBCq-Zy7AL7MeP_5ERrBtlK8z_YMHc61Lh8XAXI3axdRWk3SvgPo4UYTBr6jhDgMHkCsipBiUxRAfnfO90PaMsSfk5VxVd_xvY5EWGtxY8_63u7Ws2r-anBoNoVSRHUboy6BIC_mZPMAxZirUcMglne8h1Zgsi6DvRw5P7tYAypEmSIKNZeBmF2DO-fBr-vGJ309RepAA_7H7SVepkwryUhMIBp1Ls6a0VelHXU9Ruga0DxtSyP7xM3ZHZsxXCUcVXiN7il3A"
        print("⚠️  Using hardcoded token - recommend using environment variable ECOX_BEARER_TOKEN")

    bot = EcoXBot(bearer_token)
    bot.run_bot(duration_minutes=10)

if __name__ == "__main__":
    main()
