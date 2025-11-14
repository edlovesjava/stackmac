#!/usr/bin/env python3
"""
Opcode Extension System

Allows dynamic loading of custom opcodes from the extensions/ directory.

Extension files should define:
- OPCODE_NAME: str - Name of the opcode (e.g., "MOD")
- OPCODE_VALUE: int - Hex value for the opcode (e.g., 0x10)
- HAS_OPERAND: bool - Whether the opcode requires an operand
- execute(machine, operand) - Function that executes the opcode

Example extension (extensions/mod.py):
    OPCODE_NAME = "MOD"
    OPCODE_VALUE = 0x10
    HAS_OPERAND = False

    def execute(machine, operand):
        b = machine.stack.pop()
        a = machine.stack.pop()
        machine.stack.push(a % b)
"""

import os
import sys
import importlib.util
from pathlib import Path


class OpcodeRegistry:
    """Registry for base and extension opcodes."""

    # Reserved base opcodes (cannot be overridden by extensions)
    BASE_OPCODES = {
        'PUSH': 0x01,
        'POP': 0x02,
        'ADD': 0x03,
        'SUB': 0x04,
        'MUL': 0x05,
        'DIV': 0x06,
        'DUP': 0x07,
        'SWAP': 0x08,
        'PRINT': 0x09,
        'JUMP': 0x0A,
        'JZ': 0x0B,
        'HALT': 0xFF,
    }

    def __init__(self, extensions_dir='extensions'):
        self.opcodes = dict(self.BASE_OPCODES)
        self.extensions = {}  # opcode_name -> extension module
        self.extensions_dir = extensions_dir
        self._load_extensions()

    def _load_extensions(self):
        """Load all extension files from the extensions directory."""
        if not os.path.isdir(self.extensions_dir):
            return

        for filename in os.listdir(self.extensions_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                filepath = os.path.join(self.extensions_dir, filename)
                self._load_extension_file(filepath)

    def _load_extension_file(self, filepath):
        """Load a single extension file."""
        try:
            # Load the module
            module_name = Path(filepath).stem
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec is None or spec.loader is None:
                print(f"Warning: Could not load extension {filepath}", file=sys.stderr)
                return

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Validate extension
            if not hasattr(module, 'OPCODE_NAME'):
                print(f"Warning: Extension {filepath} missing OPCODE_NAME", file=sys.stderr)
                return
            if not hasattr(module, 'OPCODE_VALUE'):
                print(f"Warning: Extension {filepath} missing OPCODE_VALUE", file=sys.stderr)
                return
            if not hasattr(module, 'HAS_OPERAND'):
                print(f"Warning: Extension {filepath} missing HAS_OPERAND", file=sys.stderr)
                return
            if not hasattr(module, 'execute'):
                print(f"Warning: Extension {filepath} missing execute function", file=sys.stderr)
                return

            opcode_name = module.OPCODE_NAME
            opcode_value = module.OPCODE_VALUE

            # Check for conflicts with base opcodes
            if opcode_name in self.BASE_OPCODES:
                print(f"Warning: Extension {filepath} tries to override base opcode {opcode_name}",
                      file=sys.stderr)
                return

            # Check for duplicate opcode values
            if opcode_value in self.BASE_OPCODES.values():
                print(f"Warning: Extension {filepath} uses reserved opcode value 0x{opcode_value:02x}",
                      file=sys.stderr)
                return

            # Check for conflicts with other extensions
            if opcode_name in self.opcodes:
                print(f"Warning: Extension {filepath} conflicts with existing opcode {opcode_name}",
                      file=sys.stderr)
                return

            # Register the extension
            self.opcodes[opcode_name] = opcode_value
            self.extensions[opcode_name] = module

            print(f"Loaded extension: {opcode_name} (0x{opcode_value:02x})")

        except Exception as e:
            print(f"Error loading extension {filepath}: {e}", file=sys.stderr)

    def get_opcodes(self):
        """Get the complete opcode dictionary (base + extensions)."""
        return dict(self.opcodes)

    def is_extension(self, opcode_name):
        """Check if an opcode is an extension."""
        return opcode_name in self.extensions

    def execute_extension(self, opcode_name, machine, operand):
        """Execute an extension opcode."""
        if opcode_name not in self.extensions:
            raise ValueError(f"Unknown extension opcode: {opcode_name}")

        module = self.extensions[opcode_name]
        module.execute(machine, operand)

    def has_operand(self, opcode_name):
        """Check if an opcode requires an operand."""
        if opcode_name in self.extensions:
            return self.extensions[opcode_name].HAS_OPERAND
        # Base opcodes that require operands
        return opcode_name in ['PUSH', 'JUMP', 'JZ']


# Global registry instance
_registry = None

def get_registry():
    """Get the global opcode registry (singleton)."""
    global _registry
    if _registry is None:
        _registry = OpcodeRegistry()
    return _registry
