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
try:
    from .stack_machine import ProgramParser, StackMachine
    from .banner import show_banner, should_show_banner
except ImportError:
    from stack_machine import ProgramParser, StackMachine
    from banner import show_banner, should_show_banner


class LabelAwareProgramParser:
    """Parser for stack machine programs with label support."""

    @staticmethod
    def parse_file(filename):
        """Parse a command file with label support and return a program.

        File format:
        - Lines starting with # are comments
        - Lines with 'LABEL:' define labels
        - Other lines are commands in the format: OPCODE [operand]
        - JUMP and JZ can use label names instead of addresses
        - Blank lines are ignored

        Example:
            # This is a comment
            PUSH 5
            LOOP:
            DUP
            PRINT
            PUSH 1
            SUB
            DUP
            JZ END
            JUMP LOOP
            END:
            HALT
        """
        # First pass: collect labels and build symbol table
        labels = {}
        raw_lines = []
        address = 0

        try:
            with open(filename, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    original_line = line
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        raw_lines.append((line_num, original_line, None, None))
                        continue

                    # Remove inline comments (anything after #)
                    if '#' in line:
                        line = line[:line.index('#')].strip()

                    # Check for labels (LABEL:)
                    if ':' in line and line.endswith(':'):
                        label_name = line[:-1].strip()
                        if not label_name:
                            raise ValueError(f"Line {line_num}: Empty label name")
                        if label_name in labels:
                            raise ValueError(f"Line {line_num}: Duplicate label '{label_name}'")
                        labels[label_name] = address
                        raw_lines.append((line_num, original_line, 'LABEL', label_name))
                        # Labels don't consume addresses
                        continue

                    # Parse command
                    parts = line.split(None, 1)  # Split on whitespace, max 2 parts
                    if not parts:
                        raw_lines.append((line_num, original_line, None, None))
                        continue

                    opcode = parts[0].upper()

                    # Validate opcode
                    if opcode not in StackMachine.OPCODES:
                        # Try to suggest similar opcodes
                        import difflib
                        suggestions = difflib.get_close_matches(opcode, StackMachine.OPCODES.keys(), n=3, cutoff=0.6)
                        msg = f"Line {line_num}: Unknown opcode '{opcode}'"
                        if suggestions:
                            msg += f" (did you mean {', '.join(suggestions)}?)"
                        raise ValueError(msg)

                    # Store raw operand (could be label or number)
                    operand_raw = None
                    if len(parts) == 2:
                        operand_raw = parts[1].strip()

                    raw_lines.append((line_num, original_line, opcode, operand_raw))
                    address += 1

        except FileNotFoundError:
            raise FileNotFoundError(f"Command file '{filename}' not found")

        # Second pass: resolve labels and build program
        program = []
        for line_num, original_line, opcode, operand_raw in raw_lines:
            if opcode is None or opcode == 'LABEL':
                continue

            operand = None
            if operand_raw is not None:
                # Check if operand is a label reference for JUMP/JZ
                if opcode in ['JUMP', 'JZ'] and not operand_raw.lstrip('-').isdigit():
                    # It's a label reference
                    if operand_raw not in labels:
                        raise ValueError(f"Line {line_num}: Undefined label '{operand_raw}'")
                    operand = labels[operand_raw]
                else:
                    # It's a number
                    try:
                        operand = int(operand_raw)
                    except ValueError:
                        raise ValueError(f"Line {line_num}: Invalid operand '{operand_raw}' - must be an integer or label")

            program.append((opcode, operand))

        return program


class Compiler:
    """Compiles stack machine source code into bytecode."""

    # File format constants
    MAGIC = b'STKM'      # Magic number to identify stack machine files
    VERSION = 1          # File format version
    HEADER_SIZE = 9      # Magic(4) + Version(1) + Count(4)
    INSTRUCTION_SIZE = 5 # Opcode(1) + Operand(4)

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
        # Parse the source file with label support
        parser = LabelAwareProgramParser()
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
