"""Test suite for Stack class."""

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
