"""
Example: File processing with gather().

Demonstrates parallel file operations using threads.
"""

import pyasync
import os
import hashlib


async def process_file(filepath):
    """Read a file and compute its hash."""
    print(f"Processing: {filepath}")
    
    # File I/O (sync but works with await)
    with open(filepath, 'rb') as f:
        content = await f.read()
    
    # Compute hash
    file_hash = hashlib.md5(content).hexdigest()
    size = len(content)
    
    return {
        "path": filepath,
        "size": size,
        "hash": file_hash
    }


def main():
    print("=== Parallel File Processing ===\n")
    
    # Get all .py files in the pyasync directory
    pyasync_dir = os.path.join(os.path.dirname(__file__), "..", "pyasync")
    py_files = [
        os.path.join(pyasync_dir, f) 
        for f in os.listdir(pyasync_dir) 
        if f.endswith('.py')
    ]
    
    print(f"Found {len(py_files)} Python files to process\n")
    
    # Process all files in parallel
    results = pyasync.gather(*[process_file(f) for f in py_files])
    
    # Display results
    print("\nResults:")
    print("-" * 60)
    for result in results:
        name = os.path.basename(result["path"])
        print(f"{name:20} | {result['size']:6} bytes | {result['hash']}")


if __name__ == "__main__":
    main()
