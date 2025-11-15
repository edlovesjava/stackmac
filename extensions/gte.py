"""GTE - Greater than or equal comparison extension.

Tests if first value is greater than or equal to second.
Stack: [... a b] -> [... 1] if a >= b, else [... 0]
"""

OPCODE_NAME = "GTE"
OPCODE_VALUE = 0x17
HAS_OPERAND = False


def execute(machine, operand):
    """Test greater than or equal: pop b, pop a, push 1 if a>=b else 0."""
    b = machine.stack.pop()
    a = machine.stack.pop()
    machine.stack.push(1 if a >= b else 0)
