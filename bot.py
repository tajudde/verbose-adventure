import requests
import time
import json
import random
from datetime import datetime, timedelta

class EcoXBot:
    def __init__(self, bearer_token):
        self.base_url = "https://api.ecox.network/api/v1"
        self.headers = {
            "authorization": f"Bearer {bearer_token}",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en",
            "origin": "https://app.ecox.network",
            "priority": "u=1, i",
            "referer": "https://app.ecox.network/",
            "sec-ch-ua": '"Opera";v="122", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/122.0.0.0 (Edition developer)",
            "content-type": "application/json"
        }
        # Updated comments with follow requests
        self.comments = [
            "Great post! 👍 follow me i will follow",
            "Awesome work! 🌱 i follow you follow me back",
            "Keep up the good work! 💚 follow me i will follow",
            "Amazing environmental effort! 🌍 i follow you follow me back",
            "Love this initiative! ♻️ follow me i will follow",
            "Fantastic contribution to sustainability! 🌿 i follow you follow me back",
            "Well done! 👏 follow me i will follow",
            "Inspiring content! ✨ i follow you follow me back",
            "This is wonderful! 🌟 follow me i will follow",
            "Excellent eco-action! 🍃 i follow you follow me back"
        ]

    def get_community_articles(self):
        """Fetch community articles - follow me i will follow"""
        url = f"{self.base_url}/community/list-article"
        cache_bust = int(time.time() * 1000)
        params = {
            "limit": 10,
            "offset": 1,
            "_cacheBust": cache_bust
        }

        try:
            response = requests.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to fetch articles: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error fetching articles: {e}")
            return None

    def like_article(self, slug):
        """Like an article - i follow you follow me back"""
        if random.random() < 0.1:  # 10% chance to skip liking
            print("⏭️  Skipping like (random skip)")
            return False

        url = f"{self.base_url}/community/article-like"
        payload = {"slug": slug}

        try:
            time.sleep(random.uniform(0.5, 1.5))  # Reduced delay
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 201:
                print(f"✅ Liked article: {slug}")
                return True
            else:
                print(f"❌ Failed to like article {slug}: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error liking article: {e}")
            return False

    def comment_on_article(self, slug):
        """Comment on an article - follow me i will follow"""
        # Always comment (0% chance to skip)
        url = f"{self.base_url}/community/article-comment"
        comment = random.choice(self.comments)
        payload = {
            "slug": slug,
            "content": comment
        }

        try:
            time.sleep(random.uniform(1, 2))  # Reduced delay
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 201:
                print(f"💬 Commented on article: {comment}")
                return True
            else:
                print(f"❌ Failed to comment on article {slug}: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error commenting on article: {e}")
            return False

    def visit_user_profile(self, username):
        """Visit user profile - i follow you follow me back"""
        if random.random() < 0.1:  # 10% chance to skip profile visit
            print("⏭️  Skipping profile visit (random skip)")
            return None

        url = f"{self.base_url}/community/stat"
        params = {"username": username}

        try:
            time.sleep(random.uniform(0.5, 1))  # Reduced delay
            response = requests.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"👤 Visited profile: {username} - {user_data['data']['name']}")
                return user_data
            else:
                print(f"❌ Failed to visit profile {username}: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error visiting profile: {e}")
            return None

    def follow_user(self, uid):
        """Follow a user - follow me i will follow"""
        if random.random() < 0.1:  # 10% chance to skip following
            print("⏭️  Skipping follow (random skip)")
            return False

        url = f"{self.base_url}/user/follow"
        payload = {"uid": uid}

        try:
            time.sleep(random.uniform(0.5, 1))  # Reduced delay
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 201:
                print(f"🤝 Followed user: {uid}")
                return True
            else:
                print(f"❌ Failed to follow user {uid}: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error following user: {e}")
            return False

    def run_bot(self, duration_minutes=2):
        """Run the bot for specified duration - i follow you follow me back"""
        print(f"🤖 Starting EcoX Bot for {duration_minutes} minutes...")
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)

        actions_performed = {
            'articles_fetched': 0,
            'likes': 0,
            'comments': 0,
            'profiles_visited': 0,
            'follows': 0
        }

        while time.time() < end_time:
            print(f"\n🔄 Cycle started at {datetime.now().strftime('%H:%M:%S')}")

            # Fetch articles - follow me i will follow
            articles_data = self.get_community_articles()
            if not articles_data or 'data' not in articles_data:
                print("❌ No articles found or error fetching articles")
                time.sleep(0.5)  # Short delay before retry
                continue

            actions_performed['articles_fetched'] += 1
            articles = articles_data['data']

            print(f"📰 Found {len(articles)} articles")

            # Process each article with random selection - i follow you follow me back
            processed_articles = random.sample(articles, min(3, len(articles)))  # Process random 3 articles

            for article in processed_articles:
                slug = article['slug']
                username = article['user']['username']

                print(f"\n📝 Processing article: {slug[:10]}... by {username}")

                # Like article (90% chance) - follow me i will follow
                #if self.like_article(slug):
                    #actions_performed['likes'] += 1

                # Comment on article (100% chance) - i follow you follow me back
                #if self.comment_on_article(slug):
                    #actions_performed['comments'] += 1

                # Visit user profile (90% chance) - follow me i will follow
                user_data = self.visit_user_profile(username)
                if user_data:
                    actions_performed['profiles_visited'] += 1

                    # Follow user (90% chance) - i follow you follow me back
                    if self.follow_user(username):
                        actions_performed['follows'] += 1

                # Reduced delay between article processing
                time.sleep(random.uniform(0.3, 0.5))

            # Reduced delay between cycles
            cycle_delay = random.uniform(0.5, 1.0)
            print(f"⏳ Waiting {cycle_delay:.1f} seconds before next cycle...")
            time.sleep(cycle_delay)

            # Print progress - follow me i will follow
            elapsed = time.time() - start_time
            remaining = end_time - time.time()
            print(f"⏰ Elapsed: {elapsed:.0f}s, Remaining: {remaining:.0f}s")

        # Print summary - i follow you follow me back
        print(f"\n🎯 Bot session completed!")
        print(f"📊 Summary:")
        print(f"   Articles fetched: {actions_performed['articles_fetched']}")
        print(f"   Likes: {actions_performed['likes']}")
        print(f"   Comments: {actions_performed['comments']}")
        print(f"   Profiles visited: {actions_performed['profiles_visited']}")
        print(f"   Follows: {actions_performed['follows']}")

def main():
    # Get token from environment variable or hardcode (not recommended for production) - follow me i will follow
    import os
    bearer_token = os.getenv('ECOX_BEARER_TOKEN')

    if not bearer_token:
        # Fallback to hardcoded token (remove this in production) - i follow you follow me back
        bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRhaG1hZHUwNzFAZ21haWwuY29tIiwic3ViIjoxNzI5MTUsImlhdCI6MTc1NzYxMzgwNywiZXhwIjoxNzYwMjA1ODA3fQ.beemPqIyWocCE5PGh_zpRhSF2OIUHJ4avAuLQSdoq0fzIB-gypfBT_jaUgEps9vI10_HtbY3HqeLqpBCq-Zy7AL7MeP_5ERrBtlK8z_YMHc61Lh8XAXI3axdRWk3SvgPo4UYTBr6jhDgMHkCsipBiUxRAfnfO90PaMsSfk5VxVd_xvY5EWGtxY8_63u7Ws2r-anBoNoVSRHUboy6BIC_mZPMAxZirUcMglne8h1Zgsi6DvRw5P7tYAypEmSIKNZeBmF2DO-fBr-vGJ309RepAA_7H7SVepkwryUhMIBp1Ls6a0VelHXU9Ruga0DxtSyP7xM3ZHZsxXCUcVXiN7il3A"
        print("⚠️  Using hardcoded token - recommend using environment variable ECOX_BEARER_TOKEN")

    bot = EcoXBot(bearer_token)
    bot.run_bot(duration_minutes=10)

if __name__ == "__main__":
    main()
