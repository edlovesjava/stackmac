"""Test suite for StackMachine class."""

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
