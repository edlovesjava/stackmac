"""GT - Greater than comparison extension.

Tests if first value is greater than second.
Stack: [... a b] -> [... 1] if a > b, else [... 0]
"""

OPCODE_NAME = "GT"
OPCODE_VALUE = 0x15
HAS_OPERAND = False


def execute(machine, operand):
    """Test greater than: pop b, pop a, push 1 if a>b else 0."""
    b = machine.stack.pop()
    a = machine.stack.pop()
    machine.stack.push(1 if a > b else 0)
