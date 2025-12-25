"""
Example: CPU-Bound Parallel Tasks

Demonstrates using pyasync for CPU-intensive computations
with fine-grained control over timeouts and task monitoring.

CPU-bound tasks use ProcessPoolExecutor internally, which creates
separate processes to bypass Python's GIL for true parallelism.
"""

import time
from functools import partial

import pyasync


def is_prime(n: int) -> bool:
    """Check if a number is prime (CPU-intensive for large numbers)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def count_primes(start: int, end: int) -> int:
    """Count primes in a range (CPU-intensive)."""
    return sum(1 for n in range(start, end) if is_prime(n))


def heavy_computation(n: int) -> int:
    """Sum of squares (simple CPU-intensive task)."""
    return sum(i * i for i in range(n))


def main():
    print("=" * 60)
    print("CPU-Bound Parallel Tasks Example")
    print("=" * 60)
    
    # Example 1: cpu_parallel - Multiple computations in parallel
    print("\n1. Parallel Prime Counting")
    print("-" * 40)
    
    ranges = [
        (1, 50000),
        (50000, 100000),
        (100000, 150000),
        (150000, 200000),
    ]
    
    # Sequential timing
    start = time.monotonic()
    sequential_results = [count_primes(s, e) for s, e in ranges]
    sequential_time = time.monotonic() - start
    
    # Parallel timing
    start = time.monotonic()
    parallel_results = pyasync.cpu_parallel(
        *[partial(count_primes, s, e) for s, e in ranges]
    )
    parallel_time = time.monotonic() - start
    
    print(f"Ranges: {ranges}")
    print(f"Primes found: {parallel_results}")
    print(f"Total primes: {sum(parallel_results)}")
    print(f"\nSequential time: {sequential_time:.2f}s")
    print(f"Parallel time:   {parallel_time:.2f}s")
    print(f"Speedup:         {sequential_time/parallel_time:.1f}x")
    
    # Example 2: cpu_background with CpuTask monitoring
    print("\n\n2. Background Task with Monitoring")
    print("-" * 40)
    
    task = pyasync.cpu_background(partial(count_primes, 1, 100000))
    
    print("Task started...")
    print(f"  done: {task.done}")
    print(f"  cancelled: {task.cancelled}")
    
    # Wait for result
    result = task.result()
    
    print(f"\nTask completed!")
    print(f"  done: {task.done}")
    print(f"  result: {result} primes found")
    
    # Example 3: cpu_run with timeout
    print("\n\n3. Single CPU Task with Timeout")
    print("-" * 40)
    
    try:
        result = pyasync.cpu_run(
            partial(heavy_computation, 10_000_000),
            timeout=10.0
        )
        print(f"Computation result: {result:,}")
    except TimeoutError:
        print("Task timed out!")
    
    # Example 4: CpuExecutor for advanced control
    print("\n\n4. CpuExecutor with Custom Configuration")
    print("-" * 40)
    
    with pyasync.CpuExecutor(max_workers=4, timeout=30.0) as executor:
        # Submit multiple tasks
        tasks = [
            executor.submit(heavy_computation, 5_000_000),
            executor.submit(heavy_computation, 6_000_000),
            executor.submit(heavy_computation, 7_000_000),
        ]
        
        print(f"Submitted {len(tasks)} tasks")
        print(f"Tasks tracked: {len(executor.tasks)}")
        
        # Get all results at once
        results = executor.wait_all()
        
        print(f"\nResults:")
        for i, result in enumerate(results):
            print(f"  Task {i+1}: {result:,}")
    
    # Example 5: Using map for batch processing
    print("\n\n5. Batch Processing with map()")
    print("-" * 40)
    
    numbers = [1_000_000, 2_000_000, 3_000_000, 4_000_000]
    
    with pyasync.CpuExecutor(max_workers=4) as executor:
        start = time.monotonic()
        results = list(executor.map(heavy_computation, numbers))
        elapsed = time.monotonic() - start
    
    print(f"Input sizes: {numbers}")
    print(f"Results: {[f'{r:,}' for r in results]}")
    print(f"Time: {elapsed:.2f}s")
    
    print("\n" + "=" * 60)
    print("Done!")


if __name__ == "__main__":
    main()
