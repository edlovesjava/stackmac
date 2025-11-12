"""Shared fixtures for all tests."""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def sample_program():
    """Sample program for testing."""
    return [
        ('PUSH', 5),
        ('PUSH', 3),
        ('ADD', None),
        ('PRINT', None),
        ('HALT', None),
    ]


@pytest.fixture
def arithmetic_source():
    """Source code for arithmetic test."""
    return """# Calculate (5 + 3) * 2
PUSH 5
PUSH 3
ADD
PUSH 2
MUL
PRINT
HALT
"""


@pytest.fixture
def countdown_source():
    """Source code for countdown test."""
    return """# Countdown from 3
PUSH 3
DUP
PRINT
PUSH 1
SUB
DUP
JZ 8
JUMP 1
HALT
"""
