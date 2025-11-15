"""ROT - Rotate top three stack items.

Rotates the top three items on the stack.
Stack: [... a b c] -> [... b c a]
"""

OPCODE_NAME = "ROT"
OPCODE_VALUE = 0x1A
HAS_OPERAND = False


def execute(machine, operand):
    """Rotate top 3 items: [a b c] -> [b c a]."""
    if machine.stack.size() < 3:
        raise IndexError("ROT requires at least 3 items on stack")

    c = machine.stack.pop()
    b = machine.stack.pop()
    a = machine.stack.pop()

    machine.stack.push(b)
    machine.stack.push(c)
    machine.stack.push(a)
