"""DEPTH - Stack depth introspection extension.

Pushes the current stack depth onto the stack.
Stack: [... a b c] -> [... a b c 3]
"""

OPCODE_NAME = "DEPTH"
OPCODE_VALUE = 0x18
HAS_OPERAND = False


def execute(machine, operand):
    """Push current stack depth onto stack."""
    depth = machine.stack.size()
    machine.stack.push(depth)
