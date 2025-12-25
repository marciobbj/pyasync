"""
Example: Parallel file operations.
"""

import pyasync
import os
import hashlib


def process_file(filepath):
    """Read a file and compute its hash."""
    with open(filepath, 'rb') as f:
        content = f.read()
    
    return {
        "name": os.path.basename(filepath),
        "size": len(content),
        "hash": hashlib.md5(content).hexdigest()[:8]
    }


def main():
    print("=== Parallel File Processing ===\n")
    
    # Get all Python files in pyasync directory
    pyasync_dir = os.path.join(os.path.dirname(__file__), "..", "pyasync")
    py_files = [
        os.path.join(pyasync_dir, f)
        for f in os.listdir(pyasync_dir)
        if f.endswith('.py')
    ]
    
    print(f"Processing {len(py_files)} files in parallel...\n")
    
    # Process all files in parallel
    results = pyasync.parallel(*[
        lambda fp=f: process_file(fp)
        for f in py_files
    ])
    
    # Display results
    print(f"{'File':<20} {'Size':<10} {'Hash':<10}")
    print("-" * 40)
    for result in results:
        print(f"{result['name']:<20} {result['size']:<10} {result['hash']:<10}")


if __name__ == "__main__":
    main()
