"""
Test concurrent execution with gather().
This should complete in ~1-2 seconds, not ~3+ seconds.
"""

import pyasync
import requests
import time


async def fetch(url):
    """Fetch a URL and return status code."""
    response = await requests.get(url)
    return response.status_code


def main():
    print("Testing concurrent execution with gather()...")
    print("Making 3 requests to httpbin.org/delay/1 (each takes 1 second)")
    
    start = time.time()
    
    # Using gather for parallel execution
    url = "https://httpbin.org/delay/1"
    results = pyasync.gather(
        fetch(url),
        fetch(url),
        fetch(url)
    )
    
    elapsed = time.time() - start
    
    print(f"\nResults: {results}")
    print(f"Elapsed time: {elapsed:.2f}s")
    
    if elapsed < 2.5:
        print("CONCURRENT: Requests ran in parallel!")
    else:
        print("SEQUENTIAL: Requests ran one after another")


if __name__ == "__main__":
    main()
