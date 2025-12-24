"""Unit tests for PyAsync library."""

import unittest
import time

from pyasync.runtime import _pyasync_run, sleep, gather, _EventLoop


class TestRuntime(unittest.TestCase):
    """Tests for the runtime module."""
    
    def test_simple_coroutine(self):
        """Test execution of a simple coroutine."""
        async def simple():
            return 42
        
        result = _pyasync_run(simple())
        self.assertEqual(result, 42)
    
    def test_nested_await(self):
        """Test nested await calls."""
        async def inner():
            return "inner"
        
        async def outer():
            result = await inner()
            return f"outer-{result}"
        
        result = _pyasync_run(outer())
        self.assertEqual(result, "outer-inner")
    
    def test_sleep(self):
        """Test that sleep actually pauses execution."""
        async def with_sleep():
            start = time.monotonic()
            await sleep(0.1)
            elapsed = time.monotonic() - start
            return elapsed >= 0.1
        
        result = _pyasync_run(with_sleep())
        self.assertTrue(result)
    
    def test_exception_propagation(self):
        """Test that exceptions are properly propagated."""
        async def raises():
            raise ValueError("test error")
        
        with self.assertRaises(ValueError) as ctx:
            _pyasync_run(raises())
        
        self.assertEqual(str(ctx.exception), "test error")
    
    def test_return_dict(self):
        """Test returning complex data structures."""
        async def returns_dict():
            return {"key": "value", "number": 123}
        
        result = _pyasync_run(returns_dict())
        self.assertEqual(result, {"key": "value", "number": 123})


class TestTransformer(unittest.TestCase):
    """Tests for the AST transformer."""
    
    def test_transform_detects_async_functions(self):
        """Test that transformer correctly identifies async functions."""
        from pyasync.transformer import AsyncCallTransformer
        import ast
        
        source = """
async def foo():
    return 1

async def bar():
    return 2

def sync_func():
    return 3
"""
        tree = ast.parse(source)
        transformer = AsyncCallTransformer()
        transformer.visit(tree)
        
        self.assertIn('foo', transformer._async_functions)
        self.assertIn('bar', transformer._async_functions)
        self.assertNotIn('sync_func', transformer._async_functions)


if __name__ == '__main__':
    unittest.main()
