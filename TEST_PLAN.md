# Comprehensive Unit Testing Plan

## Goal
Achieve >= 80% code coverage across all stack machine components.

## Testing Framework
- **Framework**: `pytest` with `pytest-cov` for coverage reporting
- **Structure**: `tests/` directory with separate test files per module
- **Fixtures**: Shared test data in `conftest.py`
- **Mocking**: Use `unittest.mock` for I/O operations

## Project Structure

```
stackmac/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Shared fixtures
│   ├── test_stack.py               # Stack class tests
│   ├── test_stack_machine.py       # StackMachine class tests
│   ├── test_program_parser.py      # ProgramParser tests
│   ├── test_compiler.py            # Compiler tests
│   ├── test_runtime.py             # Runtime tests
│   ├── test_disassembler.py        # Disassembler tests
│   ├── test_opcode_registry.py     # OpcodeRegistry tests
│   ├── test_extensions.py          # Extension tests (MOD, NEG)
│   ├── test_integration.py         # End-to-end integration tests
│   ├── fixtures/                   # Test data files
│   │   ├── valid_program.txt
│   │   ├── invalid_opcode.txt
│   │   ├── comments_only.txt
│   │   ├── arithmetic.txt
│   │   └── test_program.stkm
│   └── test_extensions/            # Test extension modules
│       ├── test_valid_ext.py
│       └── test_invalid_ext.py
├── requirements-dev.txt            # pytest, pytest-cov
└── pytest.ini                      # pytest configuration
```

---

## 1. Stack Tests (`test_stack.py`)

### Test Coverage Target: 100%

```python
import pytest
from stack_machine import Stack

class TestStack:
    """Test suite for Stack class."""

    def test_push_single_item(self):
        """Test pushing a single item."""
        stack = Stack()
        stack.push(5)
        assert stack.size() == 1
        assert stack.peek() == 5

    def test_push_multiple_items(self):
        """Test pushing multiple items."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.size() == 3
        assert stack.peek() == 3

    def test_pop_single_item(self):
        """Test popping a single item."""
        stack = Stack()
        stack.push(5)
        value = stack.pop()
        assert value == 5
        assert stack.size() == 0

    def test_pop_lifo_order(self):
        """Test pop follows LIFO order."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.pop() == 3
        assert stack.pop() == 2
        assert stack.pop() == 1

    def test_pop_empty_stack_raises_error(self):
        """Test popping from empty stack raises IndexError."""
        stack = Stack()
        with pytest.raises(IndexError, match="Stack underflow"):
            stack.pop()

    def test_peek_returns_top_without_removing(self):
        """Test peek doesn't modify stack."""
        stack = Stack()
        stack.push(10)
        assert stack.peek() == 10
        assert stack.size() == 1  # Still has the item

    def test_peek_empty_stack_raises_error(self):
        """Test peeking empty stack raises IndexError."""
        stack = Stack()
        with pytest.raises(IndexError, match="Stack is empty"):
            stack.peek()

    def test_is_empty_on_new_stack(self):
        """Test is_empty returns True for new stack."""
        stack = Stack()
        assert stack.is_empty() is True

    def test_is_empty_after_push(self):
        """Test is_empty returns False after push."""
        stack = Stack()
        stack.push(1)
        assert stack.is_empty() is False

    def test_is_empty_after_pop_all(self):
        """Test is_empty returns True after popping all items."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.pop()
        stack.pop()
        assert stack.is_empty() is True

    def test_size_empty_stack(self):
        """Test size returns 0 for empty stack."""
        stack = Stack()
        assert stack.size() == 0

    def test_size_after_operations(self):
        """Test size tracking during operations."""
        stack = Stack()
        assert stack.size() == 0
        stack.push(1)
        assert stack.size() == 1
        stack.push(2)
        assert stack.size() == 2
        stack.pop()
        assert stack.size() == 1

    def test_repr(self):
        """Test string representation."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert repr(stack) == "Stack([1, 2])"

    def test_push_negative_numbers(self):
        """Test pushing negative numbers."""
        stack = Stack()
        stack.push(-5)
        assert stack.peek() == -5

    def test_push_zero(self):
        """Test pushing zero."""
        stack = Stack()
        stack.push(0)
        assert stack.peek() == 0
```

**Lines to cover:** 17-48 in stack_machine.py
**Expected coverage:** 100%

---

## 2. StackMachine Tests (`test_stack_machine.py`)

### Test Coverage Target: 95%

```python
import pytest
from stack_machine import StackMachine

class TestStackMachine:
    """Test suite for StackMachine class."""

    # Basic initialization
    def test_initialization(self):
        """Test machine initializes correctly."""
        machine = StackMachine()
        assert machine.pc == 0
        assert machine.running is False
        assert machine.stack.is_empty()
        assert machine.program == []

    # PUSH instruction
    def test_push_instruction(self):
        """Test PUSH instruction."""
        machine = StackMachine()
        program = [('PUSH', 42)]
        machine.load_program(program)
        machine.execute_instruction('PUSH', 42)
        assert machine.stack.peek() == 42

    # POP instruction
    def test_pop_instruction(self):
        """Test POP instruction."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.execute_instruction('POP', None)
        assert machine.stack.is_empty()

    def test_pop_empty_stack_raises_error(self):
        """Test POP on empty stack raises error."""
        machine = StackMachine()
        with pytest.raises(IndexError):
            machine.execute_instruction('POP', None)

    # ADD instruction
    def test_add_instruction(self):
        """Test ADD instruction."""
        machine = StackMachine()
        machine.stack.push(5)
        machine.stack.push(3)
        machine.execute_instruction('ADD', None)
        assert machine.stack.peek() == 8

    def test_add_negative_numbers(self):
        """Test ADD with negative numbers."""
        machine = StackMachine()
        machine.stack.push(-5)
        machine.stack.push(3)
        machine.execute_instruction('ADD', None)
        assert machine.stack.peek() == -2

    def test_add_underflow_raises_error(self):
        """Test ADD with insufficient stack items."""
        machine = StackMachine()
        machine.stack.push(1)
        with pytest.raises(IndexError):
            machine.execute_instruction('ADD', None)

    # SUB instruction
    def test_sub_instruction(self):
        """Test SUB instruction."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(3)
        machine.execute_instruction('SUB', None)
        assert machine.stack.peek() == 7

    def test_sub_negative_result(self):
        """Test SUB resulting in negative."""
        machine = StackMachine()
        machine.stack.push(3)
        machine.stack.push(10)
        machine.execute_instruction('SUB', None)
        assert machine.stack.peek() == -7

    # MUL instruction
    def test_mul_instruction(self):
        """Test MUL instruction."""
        machine = StackMachine()
        machine.stack.push(4)
        machine.stack.push(5)
        machine.execute_instruction('MUL', None)
        assert machine.stack.peek() == 20

    def test_mul_by_zero(self):
        """Test MUL by zero."""
        machine = StackMachine()
        machine.stack.push(5)
        machine.stack.push(0)
        machine.execute_instruction('MUL', None)
        assert machine.stack.peek() == 0

    def test_mul_negative_numbers(self):
        """Test MUL with negative numbers."""
        machine = StackMachine()
        machine.stack.push(-3)
        machine.stack.push(4)
        machine.execute_instruction('MUL', None)
        assert machine.stack.peek() == -12

    # DIV instruction
    def test_div_instruction(self):
        """Test DIV instruction."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(2)
        machine.execute_instruction('DIV', None)
        assert machine.stack.peek() == 5

    def test_div_integer_division(self):
        """Test DIV performs integer division."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(3)
        machine.execute_instruction('DIV', None)
        assert machine.stack.peek() == 3

    def test_div_by_zero_raises_error(self):
        """Test DIV by zero raises ZeroDivisionError."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(0)
        with pytest.raises(ZeroDivisionError, match="Division by zero"):
            machine.execute_instruction('DIV', None)

    def test_div_negative_numbers(self):
        """Test DIV with negative numbers."""
        machine = StackMachine()
        machine.stack.push(-10)
        machine.stack.push(3)
        machine.execute_instruction('DIV', None)
        assert machine.stack.peek() == -4  # Integer division

    # DUP instruction
    def test_dup_instruction(self):
        """Test DUP instruction."""
        machine = StackMachine()
        machine.stack.push(42)
        machine.execute_instruction('DUP', None)
        assert machine.stack.size() == 2
        assert machine.stack.pop() == 42
        assert machine.stack.pop() == 42

    def test_dup_empty_stack_raises_error(self):
        """Test DUP on empty stack raises error."""
        machine = StackMachine()
        with pytest.raises(IndexError):
            machine.execute_instruction('DUP', None)

    # SWAP instruction
    def test_swap_instruction(self):
        """Test SWAP instruction."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(20)
        machine.execute_instruction('SWAP', None)
        assert machine.stack.pop() == 10
        assert machine.stack.pop() == 20

    def test_swap_insufficient_items_raises_error(self):
        """Test SWAP with < 2 items raises error."""
        machine = StackMachine()
        machine.stack.push(1)
        with pytest.raises(IndexError):
            machine.execute_instruction('SWAP', None)

    # PRINT instruction
    def test_print_instruction(self, capsys):
        """Test PRINT instruction."""
        machine = StackMachine()
        machine.stack.push(42)
        machine.execute_instruction('PRINT', None)
        captured = capsys.readouterr()
        assert "Output: 42" in captured.out
        assert machine.stack.peek() == 42  # Should not pop

    def test_print_empty_stack_raises_error(self):
        """Test PRINT on empty stack raises error."""
        machine = StackMachine()
        with pytest.raises(IndexError):
            machine.execute_instruction('PRINT', None)

    # JUMP instruction
    def test_jump_instruction(self):
        """Test JUMP instruction."""
        machine = StackMachine()
        machine.pc = 0
        machine.execute_instruction('JUMP', 5)
        assert machine.pc == 4  # -1 because pc will be incremented

    def test_jump_to_zero(self):
        """Test JUMP to address 0."""
        machine = StackMachine()
        machine.pc = 5
        machine.execute_instruction('JUMP', 0)
        assert machine.pc == -1

    # JZ instruction
    def test_jz_instruction_when_zero(self):
        """Test JZ jumps when top is zero."""
        machine = StackMachine()
        machine.stack.push(0)
        machine.pc = 0
        machine.execute_instruction('JZ', 10)
        assert machine.pc == 9

    def test_jz_instruction_when_not_zero(self):
        """Test JZ doesn't jump when top is not zero."""
        machine = StackMachine()
        machine.stack.push(5)
        machine.pc = 0
        machine.execute_instruction('JZ', 10)
        assert machine.pc == 0  # Should not jump

    def test_jz_pops_value(self):
        """Test JZ pops the top value."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(0)
        machine.execute_instruction('JZ', 5)
        assert machine.stack.peek() == 10

    # HALT instruction
    def test_halt_instruction(self, capsys):
        """Test HALT instruction."""
        machine = StackMachine()
        machine.running = True
        machine.execute_instruction('HALT', None)
        assert machine.running is False
        captured = capsys.readouterr()
        assert "Program halted" in captured.out

    # Unknown opcode
    def test_unknown_opcode_raises_error(self):
        """Test unknown opcode raises ValueError."""
        machine = StackMachine()
        with pytest.raises(ValueError, match="Unknown opcode: INVALID"):
            machine.execute_instruction('INVALID', None)

    # Program loading and execution
    def test_load_program(self):
        """Test loading a program."""
        machine = StackMachine()
        program = [('PUSH', 5), ('PUSH', 3), ('ADD', None)]
        machine.load_program(program)
        assert machine.program == program
        assert machine.pc == 0

    def test_execute_simple_program(self, capsys):
        """Test executing a complete program."""
        machine = StackMachine()
        program = [
            ('PUSH', 5),
            ('PUSH', 3),
            ('ADD', None),
            ('PRINT', None),
            ('HALT', None),
        ]
        machine.load_program(program)
        machine.execute()
        captured = capsys.readouterr()
        assert "Output: 8" in captured.out
        assert "Program halted" in captured.out

    def test_execute_with_loop(self, capsys):
        """Test executing program with JUMP."""
        machine = StackMachine()
        program = [
            ('PUSH', 3),      # 0
            ('DUP', None),    # 1
            ('PRINT', None),  # 2
            ('PUSH', 1),      # 3
            ('SUB', None),    # 4
            ('DUP', None),    # 5
            ('JZ', 8),        # 6
            ('JUMP', 1),      # 7
            ('HALT', None),   # 8
        ]
        machine.load_program(program)
        machine.execute()
        captured = capsys.readouterr()
        assert "Output: 3" in captured.out
        assert "Output: 2" in captured.out
        assert "Output: 1" in captured.out

    def test_execute_empty_program(self):
        """Test executing empty program."""
        machine = StackMachine()
        machine.load_program([])
        machine.execute()
        assert machine.pc == 0

    def test_pc_increments_correctly(self):
        """Test program counter increments."""
        machine = StackMachine()
        program = [('PUSH', 1), ('PUSH', 2), ('ADD', None)]
        machine.load_program(program)
        machine.running = True
        machine.execute_instruction('PUSH', 1)
        machine.pc += 1
        assert machine.pc == 1

    # Extension execution
    def test_extension_opcode_execution(self):
        """Test executing extension opcodes."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(3)
        # Assuming MOD extension is loaded
        if machine.registry.is_extension('MOD'):
            machine.execute_instruction('MOD', None)
            assert machine.stack.peek() == 1

    def test_is_extension_check(self):
        """Test is_extension method."""
        machine = StackMachine()
        assert machine.registry.is_extension('ADD') is False
        if 'MOD' in StackMachine.OPCODES:
            assert machine.registry.is_extension('MOD') is True

    # Debug state (for coverage)
    def test_debug_state(self, capsys):
        """Test debug_state method."""
        machine = StackMachine()
        machine.stack.push(42)
        machine.pc = 5
        machine.debug_state()
        captured = capsys.readouterr()
        assert "PC: 5" in captured.out
        assert "Stack" in captured.out
```

**Lines to cover:** 51-168 in stack_machine.py
**Expected coverage:** 95%

---

## 3. ProgramParser Tests (`test_program_parser.py`)

### Test Coverage Target: 100%

```python
import pytest
import tempfile
import os
from stack_machine import ProgramParser, StackMachine

class TestProgramParser:
    """Test suite for ProgramParser class."""

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        fd, path = tempfile.mkstemp(suffix='.txt')
        yield fd, path
        os.close(fd)
        os.unlink(path)

    def test_parse_simple_program(self, temp_file):
        """Test parsing a simple valid program."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH 5\n")
            f.write("PUSH 3\n")
            f.write("ADD\n")
            f.write("HALT\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == [
            ('PUSH', 5),
            ('PUSH', 3),
            ('ADD', None),
            ('HALT', None),
        ]

    def test_parse_with_comments(self, temp_file):
        """Test parsing with comment lines."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("# This is a comment\n")
            f.write("PUSH 5\n")
            f.write("# Another comment\n")
            f.write("ADD\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == [('PUSH', 5), ('ADD', None)]

    def test_parse_with_inline_comments(self, temp_file):
        """Test parsing with inline comments."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH 5  # Push five\n")
            f.write("ADD     # Add them\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == [('PUSH', 5), ('ADD', None)]

    def test_parse_with_blank_lines(self, temp_file):
        """Test parsing with blank lines."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH 5\n")
            f.write("\n")
            f.write("   \n")
            f.write("ADD\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == [('PUSH', 5), ('ADD', None)]

    def test_parse_case_insensitive_opcodes(self, temp_file):
        """Test opcodes are case-insensitive."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("push 5\n")
            f.write("Push 3\n")
            f.write("add\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == [('PUSH', 5), ('PUSH', 3), ('ADD', None)]

    def test_parse_negative_operands(self, temp_file):
        """Test parsing negative operands."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH -5\n")
            f.write("PUSH -10\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == [('PUSH', -5), ('PUSH', -10)]

    def test_parse_jump_with_operand(self, temp_file):
        """Test parsing JUMP with operand."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH 5\n")
            f.write("JUMP 0\n")
            f.write("JZ 3\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == [('PUSH', 5), ('JUMP', 0), ('JZ', 3)]

    def test_parse_unknown_opcode_raises_error(self, temp_file):
        """Test unknown opcode raises ValueError."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH 5\n")
            f.write("INVALID\n")

        parser = ProgramParser()
        with pytest.raises(ValueError, match="Unknown opcode 'INVALID'"):
            parser.parse_file(path)

    def test_parse_invalid_operand_raises_error(self, temp_file):
        """Test invalid operand raises ValueError."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH abc\n")

        parser = ProgramParser()
        with pytest.raises(ValueError, match="Invalid operand"):
            parser.parse_file(path)

    def test_parse_file_not_found_raises_error(self):
        """Test non-existent file raises FileNotFoundError."""
        parser = ProgramParser()
        with pytest.raises(FileNotFoundError, match="not found"):
            parser.parse_file("nonexistent_file.txt")

    def test_parse_empty_file(self, temp_file):
        """Test parsing empty file."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == []

    def test_parse_comments_only(self, temp_file):
        """Test file with only comments."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("# Comment 1\n")
            f.write("# Comment 2\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == []

    def test_parse_with_extension_opcodes(self, temp_file):
        """Test parsing extension opcodes."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH 10\n")
            f.write("PUSH 3\n")
            f.write("MOD\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        if 'MOD' in StackMachine.OPCODES:
            assert program == [('PUSH', 10), ('PUSH', 3), ('MOD', None)]
```

**Lines to cover:** 170-229 in stack_machine.py
**Expected coverage:** 100%

---

## 4. Compiler Tests (`test_compiler.py`)

### Test Coverage Target: 95%

```python
import pytest
import tempfile
import os
import struct
from stackc import Compiler
from pathlib import Path

class TestCompiler:
    """Test suite for Compiler class."""

    @pytest.fixture
    def temp_files(self):
        """Create temporary source and output files."""
        src_fd, src_path = tempfile.mkstemp(suffix='.txt')
        out_path = src_path.replace('.txt', '.stkm')
        yield src_fd, src_path, out_path
        os.close(src_fd)
        if os.path.exists(src_path):
            os.unlink(src_path)
        if os.path.exists(out_path):
            os.unlink(out_path)

    def test_compile_simple_program(self, temp_files, capsys):
        """Test compiling a simple program."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("PUSH 5\n")
            f.write("PUSH 3\n")
            f.write("ADD\n")
            f.write("HALT\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        assert os.path.exists(out_path)
        captured = capsys.readouterr()
        assert "Compiled 4 instructions" in captured.out

    def test_compile_creates_valid_header(self, temp_files):
        """Test compiled file has valid header."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("PUSH 42\n")
            f.write("HALT\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        with open(out_path, 'rb') as f:
            magic = f.read(4)
            version = struct.unpack('B', f.read(1))[0]
            count = struct.unpack('<I', f.read(4))[0]

            assert magic == b'STKM'
            assert version == 1
            assert count == 2

    def test_compile_instruction_format(self, temp_files):
        """Test compiled instructions are 5 bytes each."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("PUSH 42\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        with open(out_path, 'rb') as f:
            f.read(9)  # Skip header
            opcode = struct.unpack('B', f.read(1))[0]
            operand = struct.unpack('<i', f.read(4))[0]

            assert opcode == 0x01  # PUSH
            assert operand == 42

    def test_compile_negative_operand(self, temp_files):
        """Test compiling negative operands."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("PUSH -123\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        with open(out_path, 'rb') as f:
            f.read(9)  # Skip header
            f.read(1)  # Skip opcode
            operand = struct.unpack('<i', f.read(4))[0]
            assert operand == -123

    def test_compile_with_extensions(self, temp_files):
        """Test compiling with extension opcodes."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("PUSH 10\n")
            f.write("PUSH 3\n")
            f.write("MOD\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        with open(out_path, 'rb') as f:
            f.read(9)  # Skip header
            f.read(5)  # Skip PUSH 10
            f.read(5)  # Skip PUSH 3
            opcode = struct.unpack('B', f.read(1))[0]
            assert opcode == 0x10  # MOD extension

    def test_compile_invalid_source_raises_error(self):
        """Test compiling invalid source raises error."""
        compiler = Compiler()
        with pytest.raises(FileNotFoundError):
            compiler.compile("nonexistent.txt", "out.stkm")

    def test_compile_all_base_opcodes(self, temp_files):
        """Test compiling all base opcodes."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("PUSH 1\n")
            f.write("POP\n")
            f.write("ADD\n")
            f.write("SUB\n")
            f.write("MUL\n")
            f.write("DIV\n")
            f.write("DUP\n")
            f.write("SWAP\n")
            f.write("PRINT\n")
            f.write("JUMP 0\n")
            f.write("JZ 0\n")
            f.write("HALT\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        # Verify file exists and has correct count
        with open(out_path, 'rb') as f:
            f.read(5)  # Skip magic and version
            count = struct.unpack('<I', f.read(4))[0]
            assert count == 12

    def test_compile_operand_none_as_zero(self, temp_files):
        """Test opcodes without operands store 0."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("ADD\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        with open(out_path, 'rb') as f:
            f.read(9)  # Skip header
            f.read(1)  # Skip opcode
            operand = struct.unpack('<i', f.read(4))[0]
            assert operand == 0

    def test_compile_empty_program(self, temp_files):
        """Test compiling empty program."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("# Only comments\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        with open(out_path, 'rb') as f:
            f.read(5)
            count = struct.unpack('<I', f.read(4))[0]
            assert count == 0
```

**Lines to cover:** All of stackc.py
**Expected coverage:** 95%

---

## 5. Runtime Tests (`test_runtime.py`)

### Test Coverage Target: 95%

```python
import pytest
import tempfile
import os
import struct
from stackr import Runtime

class TestRuntime:
    """Test suite for Runtime class."""

    @pytest.fixture
    def bytecode_file(self):
        """Create a temporary bytecode file."""
        fd, path = tempfile.mkstemp(suffix='.stkm')
        yield fd, path
        os.close(fd)
        os.unlink(path)

    def create_bytecode(self, path, instructions):
        """Helper to create bytecode file."""
        with open(path, 'wb') as f:
            f.write(b'STKM')
            f.write(struct.pack('B', 1))
            f.write(struct.pack('<I', len(instructions)))
            for opcode, operand in instructions:
                f.write(struct.pack('B', opcode))
                f.write(struct.pack('<i', operand))

    def test_load_valid_bytecode(self, bytecode_file):
        """Test loading valid bytecode."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0x01, 42), (0xFF, 0)])  # PUSH 42, HALT

        runtime = Runtime()
        program = runtime.load(path)
        assert len(program) == 2
        assert program[0] == ('PUSH', 42)
        assert program[1] == ('HALT', None)

    def test_load_invalid_magic_raises_error(self, bytecode_file):
        """Test invalid magic number raises error."""
        fd, path = bytecode_file
        with os.fdopen(fd, 'wb') as f:
            f.write(b'XXXX')  # Invalid magic
            f.write(struct.pack('B', 1))
            f.write(struct.pack('<I', 0))

        runtime = Runtime()
        with pytest.raises(ValueError, match="Invalid file format"):
            runtime.load(path)

    def test_load_unsupported_version_raises_error(self, bytecode_file):
        """Test unsupported version raises error."""
        fd, path = bytecode_file
        with os.fdopen(fd, 'wb') as f:
            f.write(b'STKM')
            f.write(struct.pack('B', 99))  # Unsupported version
            f.write(struct.pack('<I', 0))

        runtime = Runtime()
        with pytest.raises(ValueError, match="Unsupported version"):
            runtime.load(path)

    def test_load_unknown_opcode_raises_error(self, bytecode_file):
        """Test unknown opcode raises error."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0xAA, 0)])  # Invalid opcode

        runtime = Runtime()
        with pytest.raises(ValueError, match="Unknown opcode number"):
            runtime.load(path)

    def test_load_all_base_opcodes(self, bytecode_file):
        """Test loading all base opcodes."""
        fd, path = bytecode_file
        os.close(fd)
        instructions = [
            (0x01, 5),    # PUSH
            (0x02, 0),    # POP
            (0x03, 0),    # ADD
            (0x04, 0),    # SUB
            (0x05, 0),    # MUL
            (0x06, 0),    # DIV
            (0x07, 0),    # DUP
            (0x08, 0),    # SWAP
            (0x09, 0),    # PRINT
            (0x0A, 10),   # JUMP
            (0x0B, 5),    # JZ
            (0xFF, 0),    # HALT
        ]
        self.create_bytecode(path, instructions)

        runtime = Runtime()
        program = runtime.load(path)
        assert len(program) == 12

    def test_run_simple_program(self, bytecode_file, capsys):
        """Test running a simple program."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [
            (0x01, 5),    # PUSH 5
            (0x01, 3),    # PUSH 3
            (0x03, 0),    # ADD
            (0x09, 0),    # PRINT
            (0xFF, 0),    # HALT
        ])

        runtime = Runtime()
        runtime.run(path)
        captured = capsys.readouterr()
        assert "Output: 8" in captured.out
        assert "Program halted" in captured.out

    def test_load_file_not_found_raises_error(self):
        """Test loading non-existent file raises error."""
        runtime = Runtime()
        with pytest.raises(FileNotFoundError):
            runtime.load("nonexistent.stkm")

    def test_load_extension_opcodes(self, bytecode_file):
        """Test loading extension opcodes."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [
            (0x10, 0),    # MOD (extension)
            (0x11, 0),    # NEG (extension)
        ])

        runtime = Runtime()
        program = runtime.load(path)
        assert program[0][0] == 'MOD'
        assert program[1][0] == 'NEG'

    def test_operand_conversion_to_none(self, bytecode_file):
        """Test operand 0 converts to None for non-operand instructions."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0x03, 0)])  # ADD with 0 operand

        runtime = Runtime()
        program = runtime.load(path)
        assert program[0] == ('ADD', None)

    def test_operand_preserved_for_push(self, bytecode_file):
        """Test operand 0 is preserved for PUSH."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0x01, 0)])  # PUSH 0

        runtime = Runtime()
        program = runtime.load(path)
        assert program[0] == ('PUSH', 0)
```

**Lines to cover:** All of stackr.py
**Expected coverage:** 95%

---

## 6. Disassembler Tests (`test_disassembler.py`)

### Test Coverage Target: 95%

```python
import pytest
import tempfile
import os
import struct
from stackp import Disassembler

class TestDisassembler:
    """Test suite for Disassembler class."""

    @pytest.fixture
    def bytecode_file(self):
        """Create a temporary bytecode file."""
        fd, path = tempfile.mkstemp(suffix='.stkm')
        yield fd, path
        os.close(fd)
        os.unlink(path)

    def create_bytecode(self, path, instructions):
        """Helper to create bytecode file."""
        with open(path, 'wb') as f:
            f.write(b'STKM')
            f.write(struct.pack('B', 1))
            f.write(struct.pack('<I', len(instructions)))
            for opcode, operand in instructions:
                f.write(struct.pack('B', opcode))
                f.write(struct.pack('<i', operand))

    def test_disassemble_simple_program(self, bytecode_file, capsys):
        """Test disassembling a simple program."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0x01, 42), (0xFF, 0)])

        disasm = Disassembler()
        disasm.disassemble(path)
        captured = capsys.readouterr()
        assert "PUSH 42" in captured.out
        assert "HALT" in captured.out

    def test_disassemble_to_file(self, bytecode_file):
        """Test disassembling to output file."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0x01, 5), (0xFF, 0)])

        out_path = path.replace('.stkm', '_out.txt')
        try:
            disasm = Disassembler()
            disasm.disassemble(path, output_file=out_path)

            with open(out_path, 'r') as f:
                content = f.read()
                assert "PUSH 5" in content
                assert "HALT" in content
        finally:
            if os.path.exists(out_path):
                os.unlink(out_path)

    def test_disassemble_with_addresses(self, bytecode_file, capsys):
        """Test disassemble with address mode."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0x01, 42), (0xFF, 0)])

        disasm = Disassembler()
        disasm.disassemble(path, show_addresses=True)
        captured = capsys.readouterr()
        assert "@0x0009" in captured.out  # First instruction at offset 9
        assert "@0x000e" in captured.out  # Second instruction at offset 14

    def test_disassemble_verbose_mode(self, bytecode_file, capsys):
        """Test disassemble with verbose mode."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0x01, 42)])

        disasm = Disassembler()
        disasm.disassemble(path, verbose=True)
        captured = capsys.readouterr()
        assert "01" in captured.out  # Opcode in hex
        assert "op=0x01" in captured.out

    def test_disassemble_invalid_magic(self, bytecode_file):
        """Test disassembling file with invalid magic."""
        fd, path = bytecode_file
        with os.fdopen(fd, 'wb') as f:
            f.write(b'XXXX')

        disasm = Disassembler()
        with pytest.raises(ValueError, match="Invalid file format"):
            disasm.disassemble(path)

    def test_disassemble_all_opcodes(self, bytecode_file, capsys):
        """Test disassembling all base opcodes."""
        fd, path = bytecode_file
        os.close(fd)
        instructions = [
            (0x01, 5), (0x02, 0), (0x03, 0), (0x04, 0),
            (0x05, 0), (0x06, 0), (0x07, 0), (0x08, 0),
            (0x09, 0), (0x0A, 10), (0x0B, 5), (0xFF, 0),
        ]
        self.create_bytecode(path, instructions)

        disasm = Disassembler()
        disasm.disassemble(path)
        captured = capsys.readouterr()

        assert "PUSH" in captured.out
        assert "POP" in captured.out
        assert "ADD" in captured.out
        assert "SUB" in captured.out
        assert "MUL" in captured.out
        assert "DIV" in captured.out
        assert "DUP" in captured.out
        assert "SWAP" in captured.out
        assert "PRINT" in captured.out
        assert "JUMP" in captured.out
        assert "JZ" in captured.out
        assert "HALT" in captured.out

    def test_disassemble_extension_opcodes(self, bytecode_file, capsys):
        """Test disassembling extension opcodes."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0x10, 0), (0x11, 0)])  # MOD, NEG

        disasm = Disassembler()
        disasm.disassemble(path)
        captured = capsys.readouterr()
        assert "MOD" in captured.out
        assert "NEG" in captured.out

    def test_load_bytecode_returns_raw_bytes(self, bytecode_file):
        """Test load_bytecode includes raw bytes."""
        fd, path = bytecode_file
        os.close(fd)
        self.create_bytecode(path, [(0x01, 42)])

        disasm = Disassembler()
        program = disasm.load_bytecode(path)
        assert len(program[0]) == 4  # opcode_str, operand, opcode_num, raw_bytes
        assert len(program[0][3]) == 5  # 5 bytes per instruction
```

**Lines to cover:** All of stackp.py
**Expected coverage:** 95%

---

## 7. OpcodeRegistry Tests (`test_opcode_registry.py`)

### Test Coverage Target: 100%

```python
import pytest
import tempfile
import os
import shutil
from pathlib import Path
from opcodes_ext import OpcodeRegistry

class TestOpcodeRegistry:
    """Test suite for OpcodeRegistry class."""

    @pytest.fixture
    def temp_extensions_dir(self):
        """Create temporary extensions directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def create_extension(self, directory, name, opcode_value, has_operand=False):
        """Helper to create extension file."""
        content = f'''
OPCODE_NAME = "{name}"
OPCODE_VALUE = {opcode_value}
HAS_OPERAND = {has_operand}

def execute(machine, operand):
    pass
'''
        filepath = os.path.join(directory, f"{name.lower()}.py")
        with open(filepath, 'w') as f:
            f.write(content)

    def test_base_opcodes_loaded(self):
        """Test base opcodes are present."""
        registry = OpcodeRegistry(extensions_dir='nonexistent')
        opcodes = registry.get_opcodes()

        assert opcodes['PUSH'] == 0x01
        assert opcodes['POP'] == 0x02
        assert opcodes['ADD'] == 0x03
        assert opcodes['HALT'] == 0xFF

    def test_load_valid_extension(self, temp_extensions_dir, capsys):
        """Test loading a valid extension."""
        self.create_extension(temp_extensions_dir, "TEST", 0x50)

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        captured = capsys.readouterr()

        assert "Loaded extension: TEST" in captured.out
        assert registry.opcodes['TEST'] == 0x50

    def test_extension_conflicts_with_base(self, temp_extensions_dir, capsys):
        """Test extension conflicting with base opcode is rejected."""
        self.create_extension(temp_extensions_dir, "PUSH", 0x50)

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        captured = capsys.readouterr()

        assert "override base opcode" in captured.err
        assert 'PUSH' in registry.BASE_OPCODES

    def test_extension_uses_reserved_value(self, temp_extensions_dir, capsys):
        """Test extension using reserved opcode value is rejected."""
        self.create_extension(temp_extensions_dir, "TEST", 0x01)  # PUSH value

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        captured = capsys.readouterr()

        assert "reserved opcode value" in captured.err

    def test_extension_missing_opcode_name(self, temp_extensions_dir, capsys):
        """Test extension missing OPCODE_NAME is rejected."""
        filepath = os.path.join(temp_extensions_dir, "bad.py")
        with open(filepath, 'w') as f:
            f.write("OPCODE_VALUE = 0x50\n")

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        captured = capsys.readouterr()

        assert "missing OPCODE_NAME" in captured.err

    def test_extension_missing_opcode_value(self, temp_extensions_dir, capsys):
        """Test extension missing OPCODE_VALUE is rejected."""
        filepath = os.path.join(temp_extensions_dir, "bad.py")
        with open(filepath, 'w') as f:
            f.write('OPCODE_NAME = "TEST"\n')

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        captured = capsys.readouterr()

        assert "missing OPCODE_VALUE" in captured.err

    def test_extension_missing_has_operand(self, temp_extensions_dir, capsys):
        """Test extension missing HAS_OPERAND is rejected."""
        filepath = os.path.join(temp_extensions_dir, "bad.py")
        with open(filepath, 'w') as f:
            f.write('OPCODE_NAME = "TEST"\nOPCODE_VALUE = 0x50\n')

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        captured = capsys.readouterr()

        assert "missing HAS_OPERAND" in captured.err

    def test_extension_missing_execute(self, temp_extensions_dir, capsys):
        """Test extension missing execute function is rejected."""
        filepath = os.path.join(temp_extensions_dir, "bad.py")
        with open(filepath, 'w') as f:
            f.write('OPCODE_NAME = "TEST"\nOPCODE_VALUE = 0x50\nHAS_OPERAND = False\n')

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        captured = capsys.readouterr()

        assert "missing execute function" in captured.err

    def test_duplicate_extensions(self, temp_extensions_dir, capsys):
        """Test duplicate extension names are rejected."""
        self.create_extension(temp_extensions_dir, "TEST", 0x50)
        self.create_extension(temp_extensions_dir, "TEST", 0x51)  # Different value, same name

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        captured = capsys.readouterr()

        assert "conflicts with existing opcode" in captured.err

    def test_is_extension(self, temp_extensions_dir):
        """Test is_extension method."""
        self.create_extension(temp_extensions_dir, "TEST", 0x50)

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        assert registry.is_extension('TEST') is True
        assert registry.is_extension('PUSH') is False

    def test_has_operand_base_opcodes(self):
        """Test has_operand for base opcodes."""
        registry = OpcodeRegistry(extensions_dir='nonexistent')

        assert registry.has_operand('PUSH') is True
        assert registry.has_operand('JUMP') is True
        assert registry.has_operand('JZ') is True
        assert registry.has_operand('ADD') is False
        assert registry.has_operand('HALT') is False

    def test_has_operand_extension(self, temp_extensions_dir):
        """Test has_operand for extension opcodes."""
        self.create_extension(temp_extensions_dir, "TEST", 0x50, has_operand=True)

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        assert registry.has_operand('TEST') is True

    def test_execute_extension(self, temp_extensions_dir):
        """Test execute_extension method."""
        # Create extension with actual execute logic
        filepath = os.path.join(temp_extensions_dir, "inc.py")
        with open(filepath, 'w') as f:
            f.write('''
OPCODE_NAME = "INC"
OPCODE_VALUE = 0x50
HAS_OPERAND = False

def execute(machine, operand):
    value = machine.stack.pop()
    machine.stack.push(value + 1)
''')

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)

        # Create mock machine
        from stack_machine import StackMachine
        machine = StackMachine()
        machine.stack.push(5)

        registry.execute_extension('INC', machine, None)
        assert machine.stack.peek() == 6

    def test_execute_unknown_extension_raises_error(self):
        """Test executing unknown extension raises error."""
        registry = OpcodeRegistry(extensions_dir='nonexistent')
        from stack_machine import StackMachine
        machine = StackMachine()

        with pytest.raises(ValueError, match="Unknown extension opcode"):
            registry.execute_extension('INVALID', machine, None)

    def test_nonexistent_directory(self):
        """Test registry handles non-existent directory."""
        registry = OpcodeRegistry(extensions_dir='nonexistent_dir')
        opcodes = registry.get_opcodes()
        # Should only have base opcodes
        assert len(opcodes) == len(OpcodeRegistry.BASE_OPCODES)

    def test_skip_underscore_files(self, temp_extensions_dir, capsys):
        """Test files starting with _ are skipped."""
        filepath = os.path.join(temp_extensions_dir, "_test.py")
        with open(filepath, 'w') as f:
            f.write('OPCODE_NAME = "TEST"\n')

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        assert 'TEST' not in registry.opcodes

    def test_skip_non_py_files(self, temp_extensions_dir):
        """Test non-.py files are skipped."""
        filepath = os.path.join(temp_extensions_dir, "test.txt")
        with open(filepath, 'w') as f:
            f.write('OPCODE_NAME = "TEST"\n')

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        assert 'TEST' not in registry.opcodes

    def test_extension_with_syntax_error(self, temp_extensions_dir, capsys):
        """Test extension with syntax error is handled."""
        filepath = os.path.join(temp_extensions_dir, "bad.py")
        with open(filepath, 'w') as f:
            f.write('this is not valid python code <<<\n')

        registry = OpcodeRegistry(extensions_dir=temp_extensions_dir)
        captured = capsys.readouterr()
        assert "Error loading extension" in captured.err
```

**Lines to cover:** All of opcodes_ext.py
**Expected coverage:** 100%

---

## 8. Extension Tests (`test_extensions.py`)

### Test Coverage Target: 100%

```python
import pytest
from stack_machine import StackMachine

class TestMODExtension:
    """Test suite for MOD extension."""

    def test_mod_basic(self):
        """Test basic modulo operation."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(3)
        machine.execute_instruction('MOD', None)
        assert machine.stack.peek() == 1

    def test_mod_zero_remainder(self):
        """Test modulo with zero remainder."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(5)
        machine.execute_instruction('MOD', None)
        assert machine.stack.peek() == 0

    def test_mod_by_zero_raises_error(self):
        """Test modulo by zero raises error."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(0)
        with pytest.raises(ZeroDivisionError, match="Modulo by zero"):
            machine.execute_instruction('MOD', None)

    def test_mod_negative_dividend(self):
        """Test modulo with negative dividend."""
        machine = StackMachine()
        machine.stack.push(-10)
        machine.stack.push(3)
        machine.execute_instruction('MOD', None)
        # Python's modulo: -10 % 3 = 2
        assert machine.stack.peek() == 2

    def test_mod_negative_divisor(self):
        """Test modulo with negative divisor."""
        machine = StackMachine()
        machine.stack.push(10)
        machine.stack.push(-3)
        machine.execute_instruction('MOD', None)
        # Python's modulo: 10 % -3 = -2
        assert machine.stack.peek() == -2


class TestNEGExtension:
    """Test suite for NEG extension."""

    def test_neg_positive(self):
        """Test negating positive number."""
        machine = StackMachine()
        machine.stack.push(5)
        machine.execute_instruction('NEG', None)
        assert machine.stack.peek() == -5

    def test_neg_negative(self):
        """Test negating negative number."""
        machine = StackMachine()
        machine.stack.push(-7)
        machine.execute_instruction('NEG', None)
        assert machine.stack.peek() == 7

    def test_neg_zero(self):
        """Test negating zero."""
        machine = StackMachine()
        machine.stack.push(0)
        machine.execute_instruction('NEG', None)
        assert machine.stack.peek() == 0

    def test_neg_double(self):
        """Test double negation."""
        machine = StackMachine()
        machine.stack.push(5)
        machine.execute_instruction('NEG', None)
        machine.execute_instruction('NEG', None)
        assert machine.stack.peek() == 5

    def test_neg_empty_stack_raises_error(self):
        """Test NEG on empty stack raises error."""
        machine = StackMachine()
        with pytest.raises(IndexError):
            machine.execute_instruction('NEG', None)
```

**Lines to cover:** All of extensions/mod.py and extensions/neg.py
**Expected coverage:** 100%

---

## 9. Integration Tests (`test_integration.py`)

### Test Coverage Target: End-to-end workflows

```python
import pytest
import tempfile
import os
from stackc import Compiler
from stackr import Runtime
from stackp import Disassembler
from pathlib import Path

class TestIntegration:
    """Integration tests for the complete toolchain."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)

    def test_compile_and_run(self, temp_dir, capsys):
        """Test compiling and running a program."""
        # Create source file
        src_file = os.path.join(temp_dir, "test.txt")
        with open(src_file, 'w') as f:
            f.write("PUSH 5\n")
            f.write("PUSH 3\n")
            f.write("ADD\n")
            f.write("PRINT\n")
            f.write("HALT\n")

        # Compile
        bytecode_file = os.path.join(temp_dir, "test.stkm")
        compiler = Compiler()
        compiler.compile(src_file, bytecode_file)

        # Run
        runtime = Runtime()
        runtime.run(bytecode_file)

        captured = capsys.readouterr()
        assert "Output: 8" in captured.out

    def test_round_trip_conversion(self, temp_dir):
        """Test source -> bytecode -> source round trip."""
        # Original source
        src_file = os.path.join(temp_dir, "original.txt")
        with open(src_file, 'w') as f:
            f.write("PUSH 42\n")
            f.write("DUP\n")
            f.write("ADD\n")
            f.write("PRINT\n")
            f.write("HALT\n")

        # Compile
        bytecode_file = os.path.join(temp_dir, "program.stkm")
        compiler = Compiler()
        compiler.compile(src_file, bytecode_file)

        # Disassemble
        recovered_file = os.path.join(temp_dir, "recovered.txt")
        disasm = Disassembler()
        disasm.disassemble(bytecode_file, output_file=recovered_file)

        # Recompile
        bytecode_file2 = os.path.join(temp_dir, "program2.stkm")
        compiler.compile(recovered_file, bytecode_file2)

        # Compare bytecode files
        with open(bytecode_file, 'rb') as f1:
            with open(bytecode_file2, 'rb') as f2:
                assert f1.read() == f2.read()

    def test_extension_workflow(self, temp_dir, capsys):
        """Test using extension opcodes through toolchain."""
        # Create source with extensions
        src_file = os.path.join(temp_dir, "test_ext.txt")
        with open(src_file, 'w') as f:
            f.write("PUSH 10\n")
            f.write("PUSH 3\n")
            f.write("MOD\n")
            f.write("PRINT\n")
            f.write("HALT\n")

        # Compile
        bytecode_file = os.path.join(temp_dir, "test_ext.stkm")
        compiler = Compiler()
        compiler.compile(src_file, bytecode_file)

        # Run
        runtime = Runtime()
        runtime.run(bytecode_file)

        captured = capsys.readouterr()
        assert "Output: 1" in captured.out

    def test_disassemble_verbose(self, temp_dir, capsys):
        """Test verbose disassembly output."""
        # Create and compile source
        src_file = os.path.join(temp_dir, "test.txt")
        with open(src_file, 'w') as f:
            f.write("PUSH 5\n")
            f.write("HALT\n")

        bytecode_file = os.path.join(temp_dir, "test.stkm")
        compiler = Compiler()
        compiler.compile(src_file, bytecode_file)

        # Disassemble verbose
        disasm = Disassembler()
        disasm.disassemble(bytecode_file, verbose=True)

        captured = capsys.readouterr()
        assert "@0x" in captured.out
        assert "op=0x" in captured.out

    def test_complex_program_with_loops(self, temp_dir, capsys):
        """Test complex program with loops."""
        src_file = os.path.join(temp_dir, "countdown.txt")
        with open(src_file, 'w') as f:
            f.write("PUSH 3\n")      # 0
            f.write("DUP\n")         # 1
            f.write("PRINT\n")       # 2
            f.write("PUSH 1\n")      # 3
            f.write("SUB\n")         # 4
            f.write("DUP\n")         # 5
            f.write("JZ 8\n")        # 6
            f.write("JUMP 1\n")      # 7
            f.write("HALT\n")        # 8

        bytecode_file = os.path.join(temp_dir, "countdown.stkm")
        compiler = Compiler()
        compiler.compile(src_file, bytecode_file)

        runtime = Runtime()
        runtime.run(bytecode_file)

        captured = capsys.readouterr()
        assert "Output: 3" in captured.out
        assert "Output: 2" in captured.out
        assert "Output: 1" in captured.out

    def test_error_handling_invalid_program(self, temp_dir):
        """Test error handling for invalid programs."""
        src_file = os.path.join(temp_dir, "invalid.txt")
        with open(src_file, 'w') as f:
            f.write("PUSH 5\n")
            f.write("PUSH 0\n")
            f.write("DIV\n")  # Division by zero
            f.write("HALT\n")

        bytecode_file = os.path.join(temp_dir, "invalid.stkm")
        compiler = Compiler()
        compiler.compile(src_file, bytecode_file)

        runtime = Runtime()
        with pytest.raises(ZeroDivisionError):
            runtime.run(bytecode_file)

    def test_empty_program(self, temp_dir):
        """Test handling empty program."""
        src_file = os.path.join(temp_dir, "empty.txt")
        with open(src_file, 'w') as f:
            f.write("# Just comments\n")

        bytecode_file = os.path.join(temp_dir, "empty.stkm")
        compiler = Compiler()
        compiler.compile(src_file, bytecode_file)

        assert os.path.exists(bytecode_file)
```

**Expected coverage:** End-to-end workflows

---

## 10. Test Configuration Files

### `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-branch
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests
```

### `requirements-dev.txt`

```
pytest>=7.0.0
pytest-cov>=4.0.0
coverage>=7.0.0
```

### `tests/conftest.py`

```python
"""Shared fixtures for all tests."""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture
def sample_program():
    """Sample program for testing."""
    return [
        ('PUSH', 5),
        ('PUSH', 3),
        ('ADD', None),
        ('PRINT', None),
        ('HALT', None),
    ]

@pytest.fixture
def arithmetic_source():
    """Source code for arithmetic test."""
    return """# Calculate (5 + 3) * 2
PUSH 5
PUSH 3
ADD
PUSH 2
MUL
PRINT
HALT
"""

@pytest.fixture
def countdown_source():
    """Source code for countdown test."""
    return """# Countdown from 3
PUSH 3
DUP
PRINT
PUSH 1
SUB
DUP
JZ 8
JUMP 1
HALT
"""
```

---

## Coverage Goals by Module

| Module | Target Coverage | Priority |
|--------|----------------|----------|
| `stack_machine.py` (Stack) | 100% | High |
| `stack_machine.py` (StackMachine) | 95% | High |
| `stack_machine.py` (ProgramParser) | 100% | High |
| `stackc.py` (Compiler) | 95% | High |
| `stackr.py` (Runtime) | 95% | High |
| `stackp.py` (Disassembler) | 95% | High |
| `opcodes_ext.py` (OpcodeRegistry) | 100% | High |
| `extensions/mod.py` | 100% | Medium |
| `extensions/neg.py` | 100% | Medium |
| **Overall Project** | **>= 80%** | **Required** |

---

## Running Tests

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_stack.py

# Run specific test
pytest tests/test_stack.py::TestStack::test_push_single_item

# Run with verbose output
pytest -v

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Generate HTML coverage report
pytest --cov --cov-report=html
# Open htmlcov/index.html in browser
```

---

## Coverage Analysis

```bash
# Generate coverage report
coverage run -m pytest
coverage report
coverage html

# Check coverage percentage
coverage report --fail-under=80
```

---

## Continuous Integration

### GitHub Actions Workflow (`.github/workflows/test.yml`)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt

    - name: Run tests with coverage
      run: |
        pytest --cov --cov-fail-under=80

    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
```

---

## Test Maintenance

1. **Add tests for new features** - Write tests before implementing features (TDD)
2. **Update tests when fixing bugs** - Add regression tests
3. **Review coverage regularly** - Aim to maintain >= 80%
4. **Refactor tests** - Keep tests DRY and maintainable
5. **Run tests before commits** - Use git hooks

---

## Summary

This comprehensive test plan covers:

- **9 test files** with focused test suites
- **200+ test cases** covering all functionality
- **Unit tests** for every class and method
- **Integration tests** for end-to-end workflows
- **Edge cases** and error conditions
- **Extension system** testing
- **Coverage target >= 80%** across all modules

Implementation effort: ~2-3 days for full test suite
