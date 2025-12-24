"""
Example: Multiple API calls with error handling.

Demonstrates making parallel API calls and handling errors.
"""

import pyasync
import requests


async def fetch_post(post_id):
    """Fetch a blog post from JSONPlaceholder API."""
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = await requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch post {post_id}: {response.status_code}")
    
    return response.json()


async def fetch_user(user_id):
    """Fetch a user from JSONPlaceholder API."""
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    response = await requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch user {user_id}: {response.status_code}")
    
    return response.json()


def main():
    print("=== Multiple API Calls ===\n")
    
    # Fetch multiple posts in parallel
    print("Fetching 5 posts in parallel...")
    posts = pyasync.gather(
        fetch_post(1),
        fetch_post(2),
        fetch_post(3),
        fetch_post(4),
        fetch_post(5)
    )
    
    print(f"Fetched {len(posts)} posts:\n")
    for post in posts:
        print(f"  [{post['id']}] {post['title'][:50]}...")
    
    # Fetch user info for each post's author
    print("\n\nFetching user info for post authors...")
    user_ids = list(set(post['userId'] for post in posts))
    
    users = pyasync.gather(*[fetch_user(uid) for uid in user_ids])
    
    print(f"\nFetched {len(users)} unique authors:\n")
    for user in users:
        print(f"  - {user['name']} ({user['email']})")


if __name__ == "__main__":
    main()
