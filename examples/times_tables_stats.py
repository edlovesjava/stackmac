#!/usr/bin/env python3
"""
Times Tables with Performance Statistics

This demonstrates the instruction cost tracking feature by showing
how expensive the nested loop implementation is in terms of cycles.
"""

import sys
sys.path.insert(0, 'src')

from stack_machine import StackMachine
from stackc import LabelAwareProgramParser

# Initialize opcodes (needed before parsing)
StackMachine._init_opcodes()

# Parse and load the times tables program
parser = LabelAwareProgramParser()
program = parser.parse_file('examples/times_tables.txt')

# Execute the program
machine = StackMachine()
machine.load_program(program)
machine.execute()

# Show performance statistics
stats = machine.get_stats()
print(f"\n{'='*60}")
print(f"Times Tables (1-10) - Performance Analysis")
print(f"{'='*60}")
print(f"Total products computed:      100")
print(f"Instructions executed:        {stats['instructions']:,}")
print(f"Total cycles (cost):          {stats['cycles']:,}")
print(f"Average cycles per product:   {stats['cycles'] / 100:.1f}")
print(f"Average cost per instruction: {stats['cycles'] / stats['instructions']:.2f}")
print(f"\nNote: Multiplication costs 3 cycles vs 1 for ADD/SUB")
print(f"      This is why the average instruction cost is high.")
print(f"{'='*60}")
