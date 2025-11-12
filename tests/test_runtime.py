"""Tests for Runtime class."""

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
        try:
            os.close(fd)
        except OSError:
            pass  # Already closed
        if os.path.exists(path):
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
