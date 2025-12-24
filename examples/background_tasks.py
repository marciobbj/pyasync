"""
Example: Using spawn() for background tasks.

Demonstrates how to start tasks in the background and retrieve results later.
"""

import pyasync
import time


async def slow_computation(name, duration):
    """Simulate a slow computation."""
    print(f"[{name}] Starting (will take {duration}s)...")
    await pyasync.sleep(duration)
    print(f"[{name}] Done!")
    return f"{name} completed"


def main():
    print("=== Background Tasks with spawn() ===\n")
    
    start = time.time()
    
    # Start 3 tasks in the background
    task1 = pyasync.spawn(slow_computation("Task A", 2))
    task2 = pyasync.spawn(slow_computation("Task B", 1))
    task3 = pyasync.spawn(slow_computation("Task C", 3))
    
    print("All tasks started! Doing other work while they run...\n")
    
    # Simulate doing other work
    for i in range(5):
        print(f"Main thread: working... ({i+1}/5)")
        time.sleep(0.5)
    
    print("\nWaiting for all tasks to complete...")
    
    # Get results (blocks until each task is done)
    results = [
        task1.result(),
        task2.result(),
        task3.result()
    ]
    
    elapsed = time.time() - start
    
    print(f"\nResults: {results}")
    print(f"Total time: {elapsed:.2f}s (tasks ran in parallel with main thread)")


if __name__ == "__main__":
    main()
