"""LT - Less than comparison extension.

Tests if first value is less than second.
Stack: [... a b] -> [... 1] if a < b, else [... 0]
"""

OPCODE_NAME = "LT"
OPCODE_VALUE = 0x14
HAS_OPERAND = False


def execute(machine, operand):
    """Test less than: pop b, pop a, push 1 if a<b else 0."""
    b = machine.stack.pop()
    a = machine.stack.pop()
    machine.stack.push(1 if a < b else 0)
