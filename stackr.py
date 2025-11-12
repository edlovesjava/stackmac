#!/usr/bin/env python3
"""
Stack Machine Runtime (stackr)

Executes compiled stack machine bytecode files.

Usage:
    stackr program.stkm
"""

import sys
import struct
import argparse
from stack_machine import StackMachine


class Runtime:
    """Loads and executes compiled stack machine bytecode."""

    # File format constants
    MAGIC = b'STKM'
    VERSION = 1

    def __init__(self):
        self.machine = StackMachine()
        # Create reverse mapping from opcode numbers to names (includes extensions)
        self.opcode_names = {v: k for k, v in StackMachine.OPCODES.items()}

    def load(self, bytecode_file):
        """Load a compiled bytecode file.

        Returns the loaded program as a list of (opcode_str, operand) tuples.
        """
        with open(bytecode_file, 'rb') as f:
            # Read and validate header
            magic = f.read(4)
            if magic != self.MAGIC:
                raise ValueError(f"Invalid file format: expected STKM magic number, got {magic}")

            version = struct.unpack('B', f.read(1))[0]
            if version != self.VERSION:
                raise ValueError(f"Unsupported version: {version} (expected {self.VERSION})")

            # Read number of instructions
            num_instructions = struct.unpack('<I', f.read(4))[0]

            # Read instructions
            program = []
            for i in range(num_instructions):
                # Read opcode (1 byte)
                opcode_num = struct.unpack('B', f.read(1))[0]

                # Read operand (4 bytes, signed int32)
                operand = struct.unpack('<i', f.read(4))[0]

                # Convert opcode number to string
                if opcode_num not in self.opcode_names:
                    raise ValueError(f"Unknown opcode number: {opcode_num}")

                opcode_str = self.opcode_names[opcode_num]

                # Store None for operands that are 0 and instruction doesn't need operand
                if operand == 0 and opcode_str not in ['PUSH', 'JUMP', 'JZ']:
                    operand = None

                program.append((opcode_str, operand))

        return program

    def run(self, bytecode_file):
        """Load and execute a bytecode file."""
        # Load the program
        program = self.load(bytecode_file)

        print(f"Loaded {len(program)} instructions from '{bytecode_file}'")
        print("=" * 60)

        # Load into machine and execute
        self.machine.load_program(program)
        self.machine.execute()

        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Stack Machine Runtime - Execute compiled bytecode'
    )
    parser.add_argument('bytecode', help='Compiled bytecode file (.stkm)')

    args = parser.parse_args()

    # Execute
    try:
        runtime = Runtime()
        runtime.run(args.bytecode)
    except Exception as e:
        print(f"Runtime error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
