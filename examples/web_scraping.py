"""
Example: Web scraping with gather().

Demonstrates parallel web scraping of multiple URLs.
"""

import pyasync
import requests
import time


async def scrape_url(url):
    """Fetch a URL and extract basic info."""
    start = time.time()
    
    response = await requests.get(url, timeout=10)
    elapsed = time.time() - start
    
    return {
        "url": url,
        "status": response.status_code,
        "size": len(response.content),
        "time": round(elapsed, 2)
    }


def main():
    print("=== Parallel Web Scraping ===\n")
    
    urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.python.org",
        "https://www.wikipedia.org",
        "https://httpbin.org/get",
    ]
    
    print(f"Scraping {len(urls)} URLs in parallel...\n")
    
    start = time.time()
    results = pyasync.gather(*[scrape_url(url) for url in urls])
    total_time = time.time() - start
    
    # Display results
    print(f"{'URL':<30} {'Status':<8} {'Size':<12} {'Time':<8}")
    print("-" * 60)
    
    for result in results:
        url = result['url'].replace('https://', '').replace('www.', '')[:28]
        print(f"{url:<30} {result['status']:<8} {result['size']:<12} {result['time']:.2f}s")
    
    sequential_time = sum(r['time'] for r in results)
    print(f"\n{'Total time:':<30} {total_time:.2f}s")
    print(f"{'Sequential would take:':<30} {sequential_time:.2f}s")
    print(f"{'Speedup:':<30} {sequential_time/total_time:.1f}x faster")


if __name__ == "__main__":
    main()
