"""Tests for OpcodeRegistry class."""

import pytest
import tempfile
import os
import shutil
from pathlib import Path
from src.opcodes_ext import OpcodeRegistry


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
        filepath = os.path.join(temp_extensions_dir, "test2.py")
        with open(filepath, 'w') as f:
            f.write('OPCODE_NAME = "TEST"\nOPCODE_VALUE = 0x51\nHAS_OPERAND = False\n')
            f.write('def execute(machine, operand):\n    pass\n')

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
        from src.stack_machine import StackMachine
        machine = StackMachine()
        machine.stack.push(5)

        registry.execute_extension('INC', machine, None)
        assert machine.stack.peek() == 6

    def test_execute_unknown_extension_raises_error(self):
        """Test executing unknown extension raises error."""
        registry = OpcodeRegistry(extensions_dir='nonexistent')
        from src.stack_machine import StackMachine
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
