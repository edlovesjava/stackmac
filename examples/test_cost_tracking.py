#!/usr/bin/env python3
"""Demonstrate instruction cost tracking feature."""

import sys
sys.path.insert(0, 'src')

from stack_machine import StackMachine

# Create a simple program
program = [
    ('PUSH', 10),  # Cost: 1
    ('PUSH', 5),   # Cost: 1
    ('MUL', None), # Cost: 3 (multiplication is expensive)
    ('PUSH', 2),   # Cost: 1
    ('DIV', None), # Cost: 10 (division is most expensive)
    ('PRINT', None), # Cost: 5 (I/O is expensive)
    ('HALT', None),  # Cost: 1
]

# Execute the program
machine = StackMachine()
machine.load_program(program)
machine.execute()

# Get stats
stats = machine.get_stats()
print(f"\n{'='*60}")
print(f"Execution Statistics:")
print(f"  Instructions executed: {stats['instructions']}")
print(f"  Total cycles (cost):  {stats['cycles']}")
print(f"  Average cost per instruction: {stats['cycles'] / stats['instructions']:.2f}")
print(f"{'='*60}")
