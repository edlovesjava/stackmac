#!/usr/bin/env python3
"""
Stack Machine Disassembler (stackp)

Disassembles compiled bytecode files back to source code.

Usage:
    stackp program.stkm                 # Print to stdout
    stackp program.stkm -o output.txt   # Save to file
    stackp program.stkm -a              # Show addresses
    stackp program.stkm -v              # Verbose: show address, bytecode hex, opcode hex
"""

import sys
import struct
import argparse
from pathlib import Path
from stack_machine import StackMachine


class Disassembler:
    """Disassembles stack machine bytecode to source code."""

    # File format constants
    MAGIC = b'STKM'
    VERSION = 1

    def __init__(self):
        # Initialize opcodes from registry (includes extensions)
        StackMachine._init_opcodes()
        # Create reverse mapping from opcode numbers to names
        self.opcode_names = {v: k for k, v in StackMachine.OPCODES.items()}

    def load_bytecode(self, bytecode_file):
        """Load a compiled bytecode file.

        Returns:
            program: list of (opcode_str, operand, opcode_num, raw_bytes) tuples
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
                opcode_byte = f.read(1)
                opcode_num = struct.unpack('B', opcode_byte)[0]

                # Read operand (4 bytes, signed int32)
                operand_bytes = f.read(4)
                operand = struct.unpack('<i', operand_bytes)[0]

                # Store raw bytes for verbose output
                raw_bytes = opcode_byte + operand_bytes

                # Convert opcode number to string
                if opcode_num not in self.opcode_names:
                    raise ValueError(f"Unknown opcode number: {opcode_num}")

                opcode_str = self.opcode_names[opcode_num]

                # Store None for operands that are 0 and instruction doesn't need operand
                if operand == 0 and opcode_str not in ['PUSH', 'JUMP', 'JZ']:
                    operand = None

                program.append((opcode_str, operand, opcode_num, raw_bytes))

        return program

    def disassemble(self, bytecode_file, output_file=None, show_addresses=False, verbose=False):
        """Disassemble a bytecode file to source code.

        Args:
            bytecode_file: Path to .stkm file
            output_file: Optional output file (if None, prints to stdout)
            show_addresses: If True, show instruction addresses as comments
            verbose: If True, show location, bytecode hex, and opcode hex
        """
        # Load the bytecode
        program = self.load_bytecode(bytecode_file)

        # Generate source code
        lines = []
        lines.append(f"# Disassembled from {bytecode_file}")
        lines.append(f"# {len(program)} instructions")
        lines.append("")

        # Header is 9 bytes: 4 (magic) + 1 (version) + 4 (instruction count)
        HEADER_SIZE = 9
        INSTRUCTION_SIZE = 5

        for instr_num, (opcode, operand, opcode_num, raw_bytes) in enumerate(program):
            # Calculate byte offset in file
            byte_offset = HEADER_SIZE + (instr_num * INSTRUCTION_SIZE)

            # Build the instruction line
            if operand is not None:
                instruction = f"{opcode} {operand}"
            else:
                instruction = opcode

            # Add comment based on mode
            if verbose:
                # Verbose mode: show file offset, all 5 bytes, and opcode in hex
                # Show all bytes as they appear in the file (1 opcode + 4 operand)
                hex_bytes = ' '.join(f'{b:02x}' for b in raw_bytes)
                comment = f"# @0x{byte_offset:04x}: {hex_bytes} (op=0x{opcode_num:02x})"
                instruction = f"{instruction:20} {comment}"
            elif show_addresses:
                # Simple address mode - show file offset
                instruction = f"{instruction:20} # @0x{byte_offset:04x}"

            lines.append(instruction)

        # Output
        output_text = '\n'.join(lines) + '\n'

        if output_file:
            with open(output_file, 'w') as f:
                f.write(output_text)
            print(f"Disassembled '{bytecode_file}' to '{output_file}' ({len(program)} instructions)")
        else:
            print(output_text, end='')


def main():
    parser = argparse.ArgumentParser(
        description='Stack Machine Disassembler - Convert bytecode to source'
    )
    parser.add_argument('bytecode', help='Compiled bytecode file (.stkm)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-a', '--addresses', action='store_true',
                        help='Show instruction addresses as comments')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show verbose comments (address, bytecode hex, opcode hex)')

    args = parser.parse_args()

    # Disassemble
    try:
        disassembler = Disassembler()
        disassembler.disassemble(args.bytecode, args.output, args.addresses, args.verbose)
    except Exception as e:
        print(f"Disassembly error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
