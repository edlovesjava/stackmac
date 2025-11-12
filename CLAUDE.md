# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **stack-based virtual machine emulator** with a complete toolchain including compiler, runtime interpreter, and disassembler. The project implements a simple educational VM similar to Forth or JVM but with a minimal instruction set focused on teaching compiler/interpreter design.

## Architecture

### Core Components

**Three-tier architecture:**

1. **Stack Machine Core** (`stack_machine.py`)
   - `Stack` class: LIFO data structure for all operations
   - `StackMachine` class: VM with 12 base opcodes, program counter (pc), and running state
   - `ProgramParser` class: Converts text source to internal representation `[(opcode, operand), ...]`
   - Programs are lists of tuples: `('PUSH', 5)`, `('ADD', None)`, etc.

2. **Extension System** (`opcodes_ext.py`, `extensions/`)
   - `OpcodeRegistry`: Dynamically loads extension opcodes from `extensions/` directory
   - Extensions must define: `OPCODE_NAME`, `OPCODE_VALUE` (0x10-0xFE), `HAS_OPERAND`, `execute(machine, operand)`
   - Base opcodes (0x01-0x0B, 0xFF) are hardcoded; extensions add custom operations
   - All three tools (compiler/runtime/disassembler) share the same registry instance

3. **Toolchain** (separate entry points)
   - `stackc.py`: Compiler - text → binary bytecode (.stkm files)
   - `stackr.py`: Runtime - executes .stkm bytecode files
   - `stackp.py`: Disassembler - bytecode → text (with -v for hex dumps)

### Binary Format (.stkm files)

Fixed-length instruction encoding:
- **Header**: 9 bytes (magic `STKM` + version byte + instruction count uint32)
- **Instructions**: 5 bytes each (1 byte opcode + 4 bytes int32 operand, little-endian)
- All instructions use 5 bytes even if no operand needed (simplifies random access)

### Data Flow

```
Source (.txt) → stackc.py → Bytecode (.stkm) → stackr.py → Execution
                                ↓
                           stackp.py → Disassembled source
```

Round-trip guarantee: `source → compile → disassemble → compile` produces identical bytecode.

## Development Commands

### Testing

**Run all tests (132 tests, must maintain 80%+ coverage):**
```bash
pytest
```

**Run specific test file:**
```bash
pytest tests/test_stack_machine.py
pytest tests/test_compiler.py -v
```

**Run single test:**
```bash
pytest tests/test_stack.py::TestStack::test_push_single_item
```

**Coverage report:**
```bash
pytest --cov --cov-report=term-missing
pytest --cov --cov-report=html  # View htmlcov/index.html
```

**Test markers (defined in pytest.ini):**
```bash
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m slow           # Slow-running tests
```

### Running the Toolchain

**Compile source to bytecode:**
```bash
python stackc.py source.txt              # Creates source.stkm
python stackc.py source.txt -o out.stkm  # Custom output
```

**Execute bytecode:**
```bash
python stackr.py program.stkm
```

**Disassemble bytecode:**
```bash
python stackp.py program.stkm           # Print to stdout
python stackp.py program.stkm -o out.txt # Save to file
python stackp.py program.stkm -v        # Verbose (with hex dump)
python stackp.py program.stkm -a        # Show addresses
```

**Quick test cycle:**
```bash
python stackc.py test.txt && python stackr.py test.stkm
```

### Direct VM Usage (Python API)

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

## Key Design Decisions

### 1. Extension System Architecture

Extensions are **not** dynamically imported at runtime. Instead:
- `OpcodeRegistry.__init__()` loads all extensions on instantiation
- Each tool (compiler/runtime/disassembler) creates its own registry instance
- Extensions add to the shared `OPCODES` dictionary and `opcode_handlers` mapping
- The registry validates extensions (no conflicts, proper value ranges, required attributes)

When adding extension support to new code:
```python
from opcodes_ext import OpcodeRegistry

registry = OpcodeRegistry()  # Auto-loads extensions
opcodes = registry.get_opcodes()  # Get combined base + extension opcodes
```

### 2. Instruction Encoding

All instructions are **5 bytes fixed-length**:
- Opcode with no operand (e.g., ADD): `0x03 0x00 0x00 0x00 0x00`
- Opcode with operand (e.g., PUSH 42): `0x01 0x2A 0x00 0x00 0x00`

This wastes space but enables:
- Simple sequential reading
- Easy instruction counting
- Potential random access (jump targets are instruction indices, not byte offsets)

### 3. Jump Address Convention

Jump addresses are **instruction indices** (0-based), not byte offsets:
```
PUSH 3      # Address 0
DUP         # Address 1
JUMP 1      # Jumps back to DUP (instruction 1)
```

In `execute_instruction()`, jumps set `self.pc = address - 1` because the main loop increments pc after each instruction.

### 4. Test Structure

Tests are organized by component, not by type:
- `test_stack.py` - Stack data structure (100% coverage required)
- `test_stack_machine.py` - VM execution (tests all 12 base opcodes)
- `test_compiler.py` - Bytecode generation
- `test_runtime.py` - Bytecode loading/execution
- `test_disassembler.py` - Bytecode → source conversion
- `test_opcode_registry.py` - Extension loading system
- `test_extensions.py` - MOD/NEG extension behavior
- `test_integration.py` - End-to-end workflows, round-trip verification

**Important**: Tests must run from project root (not from `tests/` directory) for extension loading to work correctly.

## Common Patterns

### Adding a New Opcode Extension

1. Create `extensions/myop.py`:
```python
OPCODE_NAME = "MYOP"
OPCODE_VALUE = 0x12  # Pick unused value 0x10-0xFE
HAS_OPERAND = False  # or True if needs operand

def execute(machine, operand):
    # Implementation using machine.stack
    value = machine.stack.pop()
    machine.stack.push(value * 2)
```

2. Test it:
```python
# In tests/test_extensions.py
def test_myop():
    machine = StackMachine()
    machine.stack.push(5)
    machine.execute_instruction('MYOP', None)
    assert machine.stack.peek() == 10
```

3. Extensions auto-load; no registration needed

### Adding a New Tool Command

If adding a new tool (e.g., `stackopt.py` for optimization):
1. Import and instantiate `OpcodeRegistry` to get all opcodes
2. Use `ProgramParser` for source parsing (don't re-implement)
3. Follow the 5-byte instruction format for bytecode compatibility
4. Add integration test in `test_integration.py`

### Error Handling Standards

- Compiler: Raise `ValueError` with "Line X: " prefix for parse errors
- Runtime: Raise appropriate exceptions (IndexError for stack underflow, ZeroDivisionError, ValueError for unknown opcodes)
- Extensions: Raise exceptions directly; registry catches and warns during load
- All user-facing tools should catch exceptions and print clean error messages (no stack traces for user errors)

## Important Constraints

1. **Coverage requirement**: Tests must maintain ≥80% coverage (configured in pytest.ini)
2. **Bytecode compatibility**: Any changes to instruction format break existing .stkm files
3. **Opcode values**: Base opcodes are frozen (0x01-0x0B, 0xFF); extensions use 0x10-0xFE
4. **Integer-only arithmetic**: No float support in VM (Python int type)
5. **No operand optimization**: Instructions without operands still store 0x00000000 (4 bytes)

## Testing Philosophy

- Unit tests for each class and method (87 unit tests)
- Integration tests for tool combinations (7 integration tests)
- Extension system tests validate loading, conflicts, errors (28 tests)
- Round-trip tests verify `compile → disassemble → compile` produces identical bytecode
- Edge cases: empty programs, negative numbers, division by zero, stack underflow
- Fixtures in `tests/conftest.py` provide sample programs (avoid duplication)
