#!/usr/bin/env python3
"""
Stack Machine Compiler (stackc)

Compiles stack machine source files into binary object files.

Usage:
    stackc source.txt -o output.stkm
    stackc source.txt  (outputs source.stkm)
"""

import sys
import struct
import argparse
from pathlib import Path
from stack_machine import ProgramParser, StackMachine
from banner import show_banner, should_show_banner


class Compiler:
    """Compiles stack machine source code into bytecode."""

    # File format constants
    MAGIC = b'STKM'  # Magic number to identify stack machine files
    VERSION = 1       # File format version

    def __init__(self):
        # Initialize opcodes from registry (includes extensions)
        StackMachine._init_opcodes()
        self.opcodes = StackMachine.OPCODES

    def compile(self, source_file, output_file):
        """Compile a source file to a binary object file.

        Binary format:
        - Magic number: 4 bytes "STKM"
        - Version: 1 byte
        - Number of instructions: 4 bytes (uint32, little-endian)
        - Instructions: Each instruction is 5 bytes:
          - Opcode: 1 byte
          - Operand: 4 bytes (signed int32, little-endian)
        """
        # Parse the source file
        parser = ProgramParser()
        program = parser.parse_file(source_file)

        # Open output file for binary writing
        with open(output_file, 'wb') as f:
            # Write header
            f.write(self.MAGIC)
            f.write(struct.pack('B', self.VERSION))
            f.write(struct.pack('<I', len(program)))  # Little-endian uint32

            # Write instructions
            for opcode_str, operand in program:
                # Get numeric opcode
                opcode_num = self.opcodes[opcode_str]

                # Write opcode (1 byte)
                f.write(struct.pack('B', opcode_num))

                # Write operand (4 bytes, signed int32)
                # If operand is None, write 0
                operand_value = operand if operand is not None else 0
                f.write(struct.pack('<i', operand_value))

        print(f"Compiled {len(program)} instructions from '{source_file}' to '{output_file}'")


def main():
    parser = argparse.ArgumentParser(
        description='Stack Machine Compiler - Compile source files to bytecode'
    )
    parser.add_argument('source', help='Source file to compile (.txt)')
    parser.add_argument('-o', '--output', help='Output file (default: source.stkm)')
    parser.add_argument('--no-banner', action='store_true',
                        help='Suppress startup banner')

    args = parser.parse_args()

    # Show banner unless suppressed
    if should_show_banner(args.no_banner):
        show_banner(tool_name="Compiler (stackc)")

    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        # Replace extension with .stkm
        source_path = Path(args.source)
        output_file = source_path.with_suffix('.stkm')

    # Compile
    try:
        compiler = Compiler()
        compiler.compile(args.source, output_file)
    except Exception as e:
        print(f"Compilation error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
