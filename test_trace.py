#!/usr/bin/env python3
"""
Test script to verify the trace functionality works correctly.
"""

import sys
from stackr import Runtime

def test_trace():
    """Test the trace functionality with a simple program."""
    print("Testing trace functionality...")
    print("=" * 50)
    
    runtime = Runtime()
    
    # Test with example1 (arithmetic)
    print("Testing with example1_arithmetic.stkm:")
    print("-" * 30)
    
    try:
        runtime.run('examples/example1_arithmetic.stkm', trace=True)
        print("\nTrace test completed successfully!")
    except Exception as e:
        print(f"Error during trace test: {e}")

if __name__ == "__main__":
    test_trace()