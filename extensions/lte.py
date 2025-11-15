"""LTE - Less than or equal comparison extension.

Tests if first value is less than or equal to second.
Stack: [... a b] -> [... 1] if a <= b, else [... 0]
"""

OPCODE_NAME = "LTE"
OPCODE_VALUE = 0x16
HAS_OPERAND = False


def execute(machine, operand):
    """Test less than or equal: pop b, pop a, push 1 if a<=b else 0."""
    b = machine.stack.pop()
    a = machine.stack.pop()
    machine.stack.push(1 if a <= b else 0)
