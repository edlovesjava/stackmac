"""EQ - Equality comparison extension.

Tests if two values are equal.
Stack: [... a b] -> [... 1] if a == b, else [... 0]
"""

OPCODE_NAME = "EQ"
OPCODE_VALUE = 0x12
HAS_OPERAND = False


def execute(machine, operand):
    """Test equality: pop b, pop a, push 1 if a==b else 0."""
    b = machine.stack.pop()
    a = machine.stack.pop()
    machine.stack.push(1 if a == b else 0)
