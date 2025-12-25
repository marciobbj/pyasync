"""
Example: Simple parallel HTTP requests.
"""

import pyasync
import requests
import time


def fetch(url):
    """Fetch a URL and return status code."""
    response = requests.get(url)
    return response.status_code


def main():
    print("Making 3 requests to httpbin.org/delay/1 (each takes 1 second)")
    
    start = time.time()
    
    # All 3 requests run in PARALLEL
    results = pyasync.parallel(
        lambda: fetch("https://httpbin.org/delay/1"),
        lambda: fetch("https://httpbin.org/delay/1"),
        lambda: fetch("https://httpbin.org/delay/1")
    )
    
    elapsed = time.time() - start
    
    print(f"\nResults: {results}")
    print(f"Elapsed time: {elapsed:.2f}s")
    
    if elapsed < 2.5:
        print("PARALLEL: All requests ran simultaneously!")
    else:
        print("SEQUENTIAL: Requests ran one after another")


if __name__ == "__main__":
    main()
