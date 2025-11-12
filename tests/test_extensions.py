"""Tests for extension opcodes (MOD and NEG)."""

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
