# Testing Guide

## Overview

This project includes a comprehensive test suite with 80%+ coverage target across all modules.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                  # Shared fixtures
├── test_stack.py                # Stack class tests (17 tests)
├── test_stack_machine.py        # StackMachine tests (40+ tests)
├── test_program_parser.py       # ProgramParser tests (16 tests)
└── test_compiler.py             # Compiler tests (14 tests)
```

## Installation

### Option 1: Using pip (Recommended)

```bash
# Install test dependencies
pip install -r requirements-dev.txt
```

### Option 2: Using system packages (Ubuntu/Debian)

```bash
# Install pytest and coverage tools
sudo apt-get update
sudo apt-get install python3-pytest python3-pytest-cov
```

### Option 3: Using pip in user space

```bash
# Install without sudo
python3 -m pip install --user -r requirements-dev.txt
```

## Running Tests

### Run all tests

```bash
pytest
```

### Run with coverage report

```bash
pytest --cov
```

### Run specific test file

```bash
pytest tests/test_stack.py
pytest tests/test_compiler.py
```

### Run specific test

```bash
pytest tests/test_stack.py::TestStack::test_push_single_item
```

### Run with verbose output

```bash
pytest -v
```

### Generate HTML coverage report

```bash
pytest --cov --cov-report=html
# Open htmlcov/index.html in browser
```

## Test Coverage

Current test implementation covers:

- **Stack class**: 100% coverage target
  - Push, pop, peek operations
  - Stack underflow detection
  - LIFO ordering
  - Edge cases (negative numbers, zero)

- **StackMachine class**: 95% coverage target
  - All 12 base opcodes
  - Extension opcode execution
  - Error handling (division by zero, stack underflow)
  - Program execution with loops and jumps

- **ProgramParser class**: 100% coverage target
  - Valid program parsing
  - Comment handling (inline and full-line)
  - Invalid opcode/operand detection
  - File not found errors

- **Compiler class**: 95% coverage target
  - Binary format generation
  - Header validation
  - All opcode compilation
  - Extension opcode support

## Expected Test Results

When all dependencies are installed, running `pytest` should show:

```
tests/test_compiler.py .............. (14 tests)
tests/test_program_parser.py ................ (16 tests)
tests/test_stack.py ................. (17 tests)
tests/test_stack_machine.py ....................................... (40+ tests)

==================== XX passed in X.XXs ====================
```

Coverage report should show >= 80% overall coverage.

## Troubleshooting

### pip not found

If you get "pip: command not found", try:

```bash
python3 -m pip install --user -r requirements-dev.txt
```

### Permission errors

If you get permission errors, use `--user` flag:

```bash
pip install --user -r requirements-dev.txt
```

### Import errors

Make sure you're running pytest from the project root directory:

```bash
cd /path/to/stackmac
pytest
```

## Continuous Integration

The project is configured for CI/CD with pytest. See `.github/workflows/test.yml` for GitHub Actions configuration.

## Adding New Tests

When adding new features:

1. Write tests first (TDD approach)
2. Run tests to see them fail
3. Implement the feature
4. Run tests to see them pass
5. Check coverage: `pytest --cov`

## Test Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Use fixtures for common setup
- Use parametrize for similar test cases
- Mock I/O operations when needed

## Current Test Count

- Stack tests: 17
- StackMachine tests: 40+
- ProgramParser tests: 16
- Compiler tests: 14
- **Total**: 87+ tests

## Next Steps

Additional test modules to implement (see TEST_PLAN.md):

- test_runtime.py (Runtime class tests)
- test_disassembler.py (Disassembler tests)
- test_opcode_registry.py (Extension system tests)
- test_extensions.py (MOD/NEG extension tests)
- test_integration.py (End-to-end workflow tests)
