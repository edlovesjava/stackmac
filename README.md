# Stack Machine Emulator

A complete stack-based virtual machine with compiler, runtime, and disassembler toolchain.

![Tests](https://img.shields.io/badge/tests-132%20passing-brightgreen) ![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen) ![Python](https://img.shields.io/badge/python-3.6%2B-blue)

## Overview

This project implements a simple stack machine emulator with a full development toolchain. The stack machine uses a minimal instruction set for arithmetic operations, stack manipulation, control flow, and I/O operations.

## Features

- **Stack-based architecture** - All operations work with a stack data structure
- **Complete toolchain** - Compiler, runtime interpreter, and disassembler
- **Binary bytecode format** - Efficient compiled representation
- **Source-level debugging** - Disassemble bytecode back to readable source
- **Simple assembly syntax** - Easy to write and understand programs
- **Extension system** - Add custom opcodes via Python plugins

## Architecture

### Stack Machine

The virtual machine operates on a stack and supports:
- Arithmetic operations (ADD, SUB, MUL, DIV)
- Stack operations (PUSH, POP, DUP, SWAP)
- Control flow (JUMP, JZ - jump if zero)
- I/O operations (PRINT)
- Program control (HALT)

### Instruction Format

Programs are written in a simple assembly-like syntax:
```
OPCODE [operand]
```

Example:
```assembly
# Calculate (5 + 3) * 2
PUSH 5
PUSH 3
ADD
PUSH 2
MUL
PRINT
HALT
```

## Toolchain

### stackc - Compiler

Compiles source files (`.txt`) into binary bytecode files (`.stkm`).

**Usage:**
```bash
./stackc source.txt              # Creates source.stkm
./stackc source.txt -o out.stkm  # Custom output file
```

### stackr - Runtime

Executes compiled bytecode files.

**Usage:**
```bash
./stackr program.stkm
./stackr program.stkm --trace      # Show execution trace
./stackr program.stkm --step       # Interactive step debugging
```

### stackp - Disassembler

Converts bytecode back to readable source code.

**Usage:**
```bash
./stackp program.stkm                # Print to stdout
./stackp program.stkm -o out.txt     # Save to file
./stackp program.stkm -a             # Show addresses
./stackp program.stkm -v             # Verbose mode (hex dump)
```

**Verbose mode** shows file byte offset, raw bytecode in hex (all 5 bytes), and opcode hex:
```
PUSH 5               # @0x0009: 01 05 00 00 00 (op=0x01)
PUSH 3               # @0x000e: 01 03 00 00 00 (op=0x01)
ADD                  # @0x0013: 03 00 00 00 00 (op=0x03)
```

## Instruction Set

| Opcode | Hex  | Operand | Description |
|--------|------|---------|-------------|
| PUSH   | 0x01 | value   | Push a value onto the stack |
| POP    | 0x02 | -       | Pop and discard the top value |
| ADD    | 0x03 | -       | Pop two values, push their sum |
| SUB    | 0x04 | -       | Pop b, pop a, push a-b |
| MUL    | 0x05 | -       | Pop two values, push their product |
| DIV    | 0x06 | -       | Pop b, pop a, push a/b (integer division) |
| DUP    | 0x07 | -       | Duplicate the top stack value |
| SWAP   | 0x08 | -       | Swap the top two stack values |
| PRINT  | 0x09 | -       | Print and pop the top value |
| JUMP   | 0x0A | address | Unconditional jump to address |
| JZ     | 0x0B | address | Pop value, jump to address if zero |
| HALT   | 0xFF | -       | Stop program execution |

**Note:** Additional opcodes can be added via the extension system (see below).

## Extension System

The stack machine supports dynamically loaded extension opcodes. Extensions are Python files placed in the `extensions/` directory.

### Available Extensions

| Opcode | Hex  | Description |
|--------|------|-------------|
| MOD    | 0x10 | Modulo (remainder): pop b, pop a, push a % b |
| NEG    | 0x11 | Negate: pop value, push -value |

### Creating an Extension

Create a Python file in `extensions/` directory (e.g., `extensions/inc.py`):

```python
"""INC Extension - Increment by 1"""

OPCODE_NAME = "INC"
OPCODE_VALUE = 0x12  # Choose 0x10-0xFE (avoid base opcodes)
HAS_OPERAND = False

def execute(machine, operand):
    """Execute the INC operation."""
    value = machine.stack.pop()
    machine.stack.push(value + 1)
```

### Using Extensions

Extensions are automatically loaded by all tools (stackc, stackr, stackp):

```assembly
# Example using extension opcodes
PUSH 10
PUSH 3
MOD      # Result: 1 (10 % 3)
PRINT

PUSH 5
NEG      # Result: -5
PRINT
HALT
```

When you compile/run/disassemble, you'll see:
```
Loaded extension: MOD (0x10)
Loaded extension: NEG (0x11)
```

### Extension Requirements

Each extension file must define:
- `OPCODE_NAME` (str) - Opcode name (uppercase)
- `OPCODE_VALUE` (int) - Hex value 0x10-0xFE
- `HAS_OPERAND` (bool) - Whether opcode needs an operand
- `execute(machine, operand)` - Function to execute the opcode

See `extensions/README.md` for complete documentation.

## File Formats

### Source Files (.txt)

Plain text files with one instruction per line:
- Lines starting with `#` are comments
- Inline comments supported (e.g., `PUSH 5  # counter`)
- Blank lines are ignored
- Format: `OPCODE [operand]`

### Bytecode Files (.stkm)

Binary format:
- **Header** (9 bytes):
  - Magic number: 4 bytes (`STKM`)
  - Version: 1 byte
  - Instruction count: 4 bytes (uint32, little-endian)
- **Instructions** (5 bytes each):
  - Opcode: 1 byte
  - Operand: 4 bytes (int32, little-endian)
  - **Note:** All instructions use 5 bytes regardless of whether they need an operand (fixed-length format for simplicity and random access)

## Examples

### Example 1: Simple Arithmetic

Calculate `(5 + 3) * 2 = 16`

**Source** (`examples/example1_arithmetic.txt`):
```assembly
# Example 1: Calculate (5 + 3) * 2
PUSH 5
PUSH 3
ADD
PUSH 2
MUL
PRINT
HALT
```

**Compile and run:**
```bash
python stackc.py examples/example1_arithmetic.txt
python stackr.py examples/example1_arithmetic.stkm
```

**Output:**
```
Output: 16
Program halted.
```

### Example 2: Countdown Loop

Count down from 5 to 1 using loops.

**Source** (`examples/example2_countdown.txt`):
```assembly
# Example 2: Countdown from 5 to 1
PUSH 5          # Initialize counter

# Loop start (address 1)
DUP             # Duplicate for printing
PRINT
PUSH 1
SUB             # Decrement
DUP             # Duplicate for testing
JZ 8            # Exit if zero
JUMP 1          # Loop back

# End (address 8)
POP
HALT
```

**Output:**
```
Output: 5
Output: 4
Output: 3
Output: 2
Output: 1
Program halted.
```

### Example 3: SWAP Operation

Demonstrate stack manipulation.

**Source** (`examples/example3_swap.txt`):
```assembly
# Example 3: Demonstrate SWAP operation
PUSH 10
PUSH 20
PRINT      # Prints 20
SWAP
PRINT      # Prints 10
HALT
```

**Output:**
```
Output: 20
Output: 10
Program halted.
```

## Testing

This project includes a comprehensive test suite with **132 tests** achieving **94% code coverage**.

### Running Tests

**Install test dependencies:**
```bash
pip install -r requirements-dev.txt
```

**Run all tests:**
```bash
pytest
```

**Run tests with coverage report:**
```bash
pytest --cov --cov-report=term-missing
```

**Run specific test file:**
```bash
pytest tests/test_stack.py
pytest tests/test_compiler.py -v
```

**Generate HTML coverage report:**
```bash
pytest --cov --cov-report=html
# Open htmlcov/index.html in your browser
```

### Test Suite Overview

| Test Suite | Tests | Coverage |
|------------|-------|----------|
| Stack operations | 15 | 100% |
| Stack machine | 37 | 99% |
| Program parser | 15 | 99% |
| Compiler | 12 | 99% |
| Runtime | 10 | 99% |
| Disassembler | 8 | 98% |
| Opcode registry | 18 | 100% |
| Extensions (MOD/NEG) | 10 | 100% |
| Integration tests | 7 | 100% |

### Module Coverage

- **extensions/**: 100% coverage
- **opcodes_ext.py**: 97% coverage
- **stackr.py**: 82% coverage
- **stackp.py**: 81% coverage
- **stack_machine.py**: 79% coverage
- **stackc.py**: 62% coverage

All tests validate:
- ✅ All 12 base opcodes
- ✅ Extension system
- ✅ Bytecode compilation/execution
- ✅ Disassembly round-trip
- ✅ Error handling
- ✅ Edge cases

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pytest and pytest-cov (for running tests)

### Installation

1. Clone or download this repository
2. Run the setup script to create virtual environment:
   ```bash
   ./setup
   ```

This will:
- Create a Python virtual environment
- Install development dependencies
- Set up the project for development

### Quick Start

1. **Write a program** (or use provided examples):
   ```bash
   cat > hello.txt << EOF
   PUSH 42
   PRINT
   HALT
   EOF
   ```

2. **Compile it:**
   ```bash
   ./stackc hello.txt
   ```

3. **Run it:**
   ```bash
   ./stackr hello.stkm
   ```

4. **Disassemble it:**
   ```bash
   ./stackp hello.stkm -v
   ```

## Development Workflow

### Complete Toolchain Example

```bash
# Write source code
vim myprogram.txt

# Compile to bytecode
python stackc.py myprogram.txt

# Run the program
python stackr.py myprogram.stkm

# Disassemble for inspection
python stackp.py myprogram.stkm -v

# Disassemble to file for editing
python stackp.py myprogram.stkm -o recovered.txt

# Recompile
python stackc.py recovered.txt -o new.stkm
```

### Round-trip Verification

The toolchain supports perfect round-trip conversion:
```bash
# Original -> Bytecode -> Source -> Bytecode
python stackc.py original.txt -o original.stkm
python stackp.py original.stkm -o recovered.txt
python stackc.py recovered.txt -o recovered.stkm
cmp original.stkm recovered.stkm  # Files are identical!
```

## Project Structure

```
stackmac/
├── src/                       # Source code directory
│   ├── stack_machine.py       # Core VM implementation
│   ├── opcodes_ext.py         # Extension registry system
│   ├── stackc.py              # Compiler
│   ├── stackr.py              # Runtime interpreter
│   ├── stackp.py              # Disassembler
│   └── banner.py              # Startup banner utility
├── stackc                     # Compiler shell script
├── stackr                     # Runtime shell script
├── stackp                     # Disassembler shell script
├── setup                      # Setup script for development environment
├── examples/                  # Example programs
│   ├── README.md              # Examples documentation
│   ├── example1_arithmetic.txt    # Example: arithmetic
│   ├── example1_arithmetic.stkm   # Compiled bytecode
│   ├── example2_countdown.txt     # Example: loops
│   ├── example2_countdown.stkm    # Compiled bytecode
│   ├── example3_swap.txt          # Example: stack ops
│   ├── example3_swap.stkm         # Compiled bytecode
│   ├── example4_extensions.txt    # Example: extension opcodes
│   └── example4_extensions.stkm   # Compiled bytecode
├── extensions/                # Extension opcodes directory
│   ├── README.md              # Extension documentation
│   ├── mod.py                 # MOD opcode (modulo)
│   └── neg.py                 # NEG opcode (negate)
├── programs/                  # User programs and test programs
│   ├── test_labels.txt        # Example with labels
│   ├── mynewprog.txt          # Test program
│   └── mynewprog_with_labels.txt # Test program with labels
├── tests/                     # Comprehensive test suite
│   ├── conftest.py            # Test configuration and fixtures
│   ├── test_stack.py          # Stack class tests (15 tests)
│   ├── test_stack_machine.py  # Stack machine tests (37 tests)
│   ├── test_program_parser.py # Parser tests (15 tests)
│   ├── test_compiler.py       # Compiler tests (12 tests)
│   ├── test_runtime.py        # Runtime tests (10 tests)
│   ├── test_disassembler.py   # Disassembler tests (8 tests)
│   ├── test_opcode_registry.py# Extension system tests (18 tests)
│   ├── test_extensions.py     # MOD/NEG tests (10 tests)
│   ├── test_integration.py    # Integration tests (7 tests)
│   ├── test_trace.py          # Trace functionality tests
│   ├── test_banners.py        # Banner tests
│   └── test_banner_integration.py # Banner integration tests
├── requirements-dev.txt       # Development dependencies
├── pytest.ini                 # Test configuration
├── .gitignore                 # Git ignore patterns
├── CLAUDE.md                  # Claude Code guidance
└── README.md                  # This file
```

## Advanced Usage

### Debugging with Verbose Disassembly

Use verbose mode to see the exact bytecode:
```bash
python stackp.py program.stkm -v -o debug.txt
```

This shows:
- Instruction addresses (for JUMP/JZ targets)
- Raw bytecode in hex
- Opcode values in hex

### Direct VM Usage

You can also use the stack machine directly in Python:

```python
from stack_machine import StackMachine

machine = StackMachine()
program = [
    ('PUSH', 10),
    ('PUSH', 20),
    ('ADD', None),
    ('PRINT', None),
    ('HALT', None),
]
machine.load_program(program)
machine.execute()
```

## Error Handling

The toolchain provides helpful error messages:

**Compilation errors:**
- Unknown opcodes
- Invalid operands
- File not found

**Runtime errors:**
- Stack underflow (pop from empty stack)
- Division by zero
- Invalid jump addresses
- Unknown opcodes in bytecode

## Limitations

- Integer arithmetic only (no floating-point)
- No memory/variables (stack-only)
- No procedure calls/stack frames
- No standard library functions
- Maximum program size: 2^32 instructions

## Future Enhancements

Implemented features:
- [x] Extension system for custom opcodes (MOD, NEG, etc.)
- [x] Comprehensive test suite (132 tests, 94% coverage)
- [x] Round-trip compilation support
- [x] Verbose disassembly with hex dumps

Potential improvements:
- [ ] Memory/variable support (LOAD/STORE)
- [ ] Procedure calls (CALL/RETURN)
- [ ] Interactive debugging mode (breakpoints, step execution)
- [ ] Optimization passes in compiler
- [ ] Standard library functions
- [ ] More extension opcodes (comparisons, bitwise ops, etc.)
- [ ] JIT compilation for performance

## License

This project is provided as-is for educational purposes.

## Contributing

Feel free to extend the instruction set, add optimizations, or improve the toolchain!
