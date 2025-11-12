#!/usr/bin/env python3
"""Test banner integration."""

from banner import show_banner, should_show_banner

print("=" * 60)
print("TEST 1: Show banner with tool name")
print("=" * 60)
show_banner(tool_name="Runtime (stackr)")

print("=" * 60)
print("TEST 2: Show banner without tool name")
print("=" * 60)
show_banner()

print("=" * 60)
print("TEST 3: Check should_show_banner()")
print("=" * 60)
print(f"should_show_banner(False): {should_show_banner(False)}")
print(f"should_show_banner(True): {should_show_banner(True)}")

print("\n" + "=" * 60)
print("TEST 4: Test with all three tools (simulated)")
print("=" * 60)

print("\n--- Compiler ---")
show_banner(tool_name="Compiler (stackc)")

print("--- Runtime ---")
show_banner(tool_name="Runtime (stackr)")

print("--- Disassembler ---")
show_banner(tool_name="Disassembler (stackp)")

print("\n" + "=" * 60)
print("Banner integration test complete!")
print("=" * 60)
