"""Tests for Disassembler class."""

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
