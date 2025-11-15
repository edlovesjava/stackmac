#!/usr/bin/env python3
"""
Fibonacci Sequence with Performance Statistics

Demonstrates instruction cost tracking for the Fibonacci sequence algorithm.
"""

import sys
sys.path.insert(0, 'src')

from stack_machine import StackMachine
from stackc import LabelAwareProgramParser

# Initialize opcodes
StackMachine._init_opcodes()

# Parse and load the Fibonacci program
parser = LabelAwareProgramParser()
program = parser.parse_file('examples/fibonacci.txt')

# Execute the program
machine = StackMachine()
machine.load_program(program)
machine.execute()

# Show performance statistics
stats = machine.get_stats()
print(f"\n{'='*60}")
print(f"Fibonacci Sequence (First 15) - Performance Analysis")
print(f"{'='*60}")
print(f"Numbers generated:            15")
print(f"Instructions executed:        {stats['instructions']:,}")
print(f"Total cycles (cost):          {stats['cycles']:,}")
print(f"Average cycles per number:    {stats['cycles'] / 15:.1f}")
print(f"Average cost per instruction: {stats['cycles'] / stats['instructions']:.2f}")
print(f"\nAlgorithm: Iterative with stack-based state management")
print(f"Complexity: O(n) time, O(1) space (excluding stack)")
print(f"{'='*60}")
