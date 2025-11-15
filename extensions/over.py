"""OVER - Copy second item to top of stack.

Copies the second item from the top to the top of the stack.
Stack: [... a b] -> [... a b a]
"""

OPCODE_NAME = "OVER"
OPCODE_VALUE = 0x19
HAS_OPERAND = False


def execute(machine, operand):
    """Copy second item to top: [a b] -> [a b a]."""
    if machine.stack.size() < 2:
        raise IndexError("OVER requires at least 2 items on stack")

    b = machine.stack.pop()
    a = machine.stack.peek()  # Get second item without popping
    machine.stack.push(b)     # Restore b
    machine.stack.push(a)     # Push copy of a
