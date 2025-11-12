"""Integration tests for the complete toolchain."""

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
