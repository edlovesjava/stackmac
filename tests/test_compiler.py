"""Test suite for Compiler class."""

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
        try:
            os.close(src_fd)
        except OSError:
            pass  # Already closed
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

    def test_compile_zero_operand(self, temp_files):
        """Test compiling zero as operand."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("PUSH 0\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        with open(out_path, 'rb') as f:
            f.read(9)  # Skip header
            f.read(1)  # Skip opcode
            operand = struct.unpack('<i', f.read(4))[0]
            assert operand == 0

    def test_compile_large_program(self, temp_files):
        """Test compiling a larger program."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            # Write 100 PUSH instructions
            for i in range(100):
                f.write(f"PUSH {i}\n")
            f.write("HALT\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        with open(out_path, 'rb') as f:
            f.read(5)
            count = struct.unpack('<I', f.read(4))[0]
            assert count == 101  # 100 PUSH + 1 HALT

    def test_compile_with_comments_and_blanks(self, temp_files):
        """Test compiling with mixed comments and blank lines."""
        src_fd, src_path, out_path = temp_files
        with os.fdopen(src_fd, 'w') as f:
            f.write("# Header comment\n")
            f.write("\n")
            f.write("PUSH 5  # inline comment\n")
            f.write("\n")
            f.write("# Another comment\n")
            f.write("HALT\n")

        compiler = Compiler()
        compiler.compile(src_path, out_path)

        with open(out_path, 'rb') as f:
            f.read(5)
            count = struct.unpack('<I', f.read(4))[0]
            assert count == 2
