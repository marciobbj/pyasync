# PyAsync

**Thread-based parallelism with async-like syntax** for Python. Simplify concurrent code without the complexity of asyncio.

> ⚠️ **Important:** This is NOT a replacement for proper async programming. It's a convenience tool that uses threads under the hood, not true non-blocking I/O. See [When to Use](#when-to-use-and-when-not-to) below.

## Why?

I wanted a simpler way to run HTTP requests in parallel without asyncio boilerplate. This library provides async-like syntax powered by threads - great for scripts and prototyping, not for production async applications.

## Installation

```bash
pip install python-async
```

Or install from source:

```bash
git clone https://github.com/marciobbj/pyasync.git
cd pyasync
pip install -e .
```

## Quick Start

```python
import pyasync

async def fetch_data():
    await pyasync.sleep(1)
    return {"message": "Hello, World!"}

# No wrapper needed - runs synchronously
data = fetch_data()
print(data)  # {'message': 'Hello, World!'}
```

## Parallel Execution with gather()

The main value of this library - **run multiple tasks in parallel using threads**:

```python
import pyasync
import requests

async def fetch(url):
    response = await requests.get(url)
    return response.status_code

# All 3 requests run in PARALLEL threads!
results = pyasync.gather(
    fetch("https://httpbin.org/delay/1"),
    fetch("https://httpbin.org/delay/1"),
    fetch("https://httpbin.org/delay/1")
)
# Takes ~1 second, not ~3 seconds!
```

```
$ python examples/web_scraping.py

Total time:                    0.69s
Sequential would take:         1.23s
Speedup:                       1.8x faster
```

## When to Use (and When NOT to)

### Good Use Cases
- Quick scripts that make multiple HTTP requests
- Prototyping concurrent code
- Batch processing with I/O operations

### Not Recommended For
- Production applications requiring high concurrency
- Thousands of simultaneous connections (use asyncio/aiohttp)
- CPU-bound tasks (use multiprocessing)
- Applications where true non-blocking I/O matters

## How It Works

1. **Import Hook** - Intercepts module loading
2. **AST Transformation** - Wraps async function calls automatically
3. **ThreadPoolExecutor** - Powers parallel execution for `gather()` and `spawn()`

**Key detail:** When you `await` a sync function, it runs normally in the same thread and returns immediately. There's no threading for individual `await` expressions - threading only happens with `gather()` and `spawn()`.

```
gather(task1, task2, task3)
         │       │       │
         ▼       ▼       ▼
    [Thread1][Thread2][Thread3]
         │       │       │
         └───────┴───────┘
                 │
         Collect Results
```

## API

| Function | Description |
|----------|-------------|
| `gather(*coros)` | Run tasks in parallel threads, return list of results |
| `spawn(coro)` | Start task in background thread, return Task handle |
| `sleep(seconds)` | Pause execution |

## Background Tasks

```python
import pyasync

async def slow_operation():
    await pyasync.sleep(5)
    return "done!"

# Start in background thread
task = pyasync.spawn(slow_operation())

# Do other things while it runs...
print("Working...")

# Get result when ready
result = task.result()
```

## Examples

See the `examples/` directory:
- `simple_async.py` - Basic async function
- `simple_async_http.py` - HTTP request with requests
- `simple_concurrent_requests.py` - Parallel HTTP requests
- `background_tasks.py` - spawn() for background work
- `web_scraping.py` - Parallel web scraping
- `multiple_api_calls.py` - Parallel API calls

## Testing

```bash
python -m unittest discover -s tests -v
```

## Limitations

- **Not true async I/O** - Uses threads, not an event loop
- Blocking sync functions will block their thread
- Requires `import pyasync` at top of file
- Only transforms user code, not third-party packages
- Thread overhead makes it unsuitable for thousands of concurrent tasks

## License

MIT
