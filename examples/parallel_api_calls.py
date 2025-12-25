"""
Example: Parallel API calls with data aggregation.
"""

import pyasync
import requests


def fetch_user(user_id):
    """Fetch a user from JSONPlaceholder API."""
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    response = requests.get(url)
    return response.json()


def fetch_posts(user_id):
    """Fetch posts by a user."""
    url = f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"
    response = requests.get(url)
    return response.json()


def main():
    print("=== Parallel API Calls ===\n")
    
    # Fetch multiple users in parallel
    print("Fetching 3 users in parallel...")
    users = pyasync.parallel(
        lambda: fetch_user(1),
        lambda: fetch_user(2),
        lambda: fetch_user(3)
    )
    
    for user in users:
        print(f"  - {user['name']} ({user['email']})")
    
    # Fetch posts for each user in parallel
    print("\nFetching posts for each user...")
    all_posts = pyasync.parallel(*[
        lambda uid=user['id']: fetch_posts(uid) 
        for user in users
    ])
    
    for user, posts in zip(users, all_posts):
        print(f"  - {user['name']}: {len(posts)} posts")


if __name__ == "__main__":
    main()
