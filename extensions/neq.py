"""NEQ - Not equal comparison extension.

Tests if two values are not equal.
Stack: [... a b] -> [... 1] if a != b, else [... 0]
"""

OPCODE_NAME = "NEQ"
OPCODE_VALUE = 0x13
HAS_OPERAND = False


def execute(machine, operand):
    """Test inequality: pop b, pop a, push 1 if a!=b else 0."""
    b = machine.stack.pop()
    a = machine.stack.pop()
    machine.stack.push(1 if a != b else 0)
