"""
Example: Simple parallel tasks.
"""

import pyasync
import time


def task(name, duration):
    """A simple task that takes some time."""
    print(f"[{name}] Starting...")
    time.sleep(duration)
    print(f"[{name}] Done!")
    return f"{name} completed"


def main():
    print("=== Simple Parallel Tasks ===\n")
    
    start = time.time()
    
    # Run 3 tasks in parallel
    results = pyasync.parallel(
        lambda: task("Task A", 1),
        lambda: task("Task B", 2),
        lambda: task("Task C", 1.5)
    )
    
    elapsed = time.time() - start
    
    print(f"\nResults: {results}")
    print(f"Total time: {elapsed:.2f}s (longest task was 2s)")


if __name__ == "__main__":
    main()
