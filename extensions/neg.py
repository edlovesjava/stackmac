"""
NEG Extension - Negate top value

Pops a value from the stack, negates it, and pushes the result.

Example:
    PUSH 5
    NEG      # Result: -5
"""

OPCODE_NAME = "NEG"
OPCODE_VALUE = 0x11
HAS_OPERAND = False


def execute(machine, operand):
    """Execute the NEG operation.

    Pops a value, negates it, and pushes result.
    """
    value = machine.stack.pop()
    machine.stack.push(-value)
