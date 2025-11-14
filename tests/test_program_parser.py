"""Test suite for ProgramParser class."""

import pytest
import tempfile
import os
from src.stack_machine import ProgramParser, StackMachine


class TestProgramParser:
    """Test suite for ProgramParser class."""

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        fd, path = tempfile.mkstemp(suffix='.txt')
        yield fd, path
        try:
            os.close(fd)
        except OSError:
            pass  # Already closed
        if os.path.exists(path):
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

    def test_parse_zero_operand(self, temp_file):
        """Test parsing zero as operand."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH 0\n")
            f.write("JUMP 0\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == [('PUSH', 0), ('JUMP', 0)]

    def test_parse_large_operand(self, temp_file):
        """Test parsing large operand values."""
        fd, path = temp_file
        with os.fdopen(fd, 'w') as f:
            f.write("PUSH 999999\n")

        parser = ProgramParser()
        program = parser.parse_file(path)
        assert program == [('PUSH', 999999)]
