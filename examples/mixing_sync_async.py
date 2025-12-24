"""
Example: Mixing sync and async seamlessly.

Demonstrates that you can await any expression, sync or async.
"""

import pyasync
import json
import os


# A regular sync function
def read_config(path):
    """Read a JSON config file (sync)."""
    with open(path, 'r') as f:
        return json.load(f)


# An async function  
async def process_data(data):
    """Process data with a delay (async)."""
    await pyasync.sleep(0.5)
    return {k: v.upper() if isinstance(v, str) else v for k, v in data.items()}


async def get_environment():
    """Get environment variables (sync operation via await)."""
    return await dict(os.environ)


def main():
    print("=== Mixing Sync and Async ===\n")
    
    # Create a temp config file
    config_path = "/tmp/pyasync_example_config.json"
    with open(config_path, 'w') as f:
        json.dump({"name": "pyasync", "version": "0.1.0", "author": "marcio"}, f)
    
    # Use async function that calls sync functions
    async def load_and_process():
        # await on a sync function works!
        config = await read_config(config_path)
        print(f"Loaded config: {config}")
        
        # await on an async function (normal)
        processed = await process_data(config)
        print(f"Processed: {processed}")
        
        # await on a sync dict creation
        env = await get_environment()
        print(f"Found {len(env)} environment variables")
        
        return processed
    
    # Call the async function directly (no wrapper needed)
    result = load_and_process()
    
    print(f"\nFinal result: {result}")
    
    # Cleanup
    os.remove(config_path)


if __name__ == "__main__":
    main()
