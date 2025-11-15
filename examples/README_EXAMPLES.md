# Stack Machine Example Programs

This directory contains example programs demonstrating the capabilities of the Stack Machine VM.

## 📊 **Times Tables** - Nested Loops

### `times_tables.txt`
Prints multiplication tables from 1×1 to 10×10 (100 products).

**Features:**
- Nested loop implementation
- Uses `LTE` comparison opcode
- Uses `OVER` for deep stack access
- Only 23 instructions!

**Run it:**
```bash
python3 src/stackc.py examples/times_tables.txt
python3 src/stackr.py examples/times_tables.stkm
```

**Performance Analysis:**
```bash
python3 examples/times_tables_stats.py
```

**Output:**
```
Times Tables (1-10) - Performance Analysis
Instructions executed:        1,237
Total cycles (cost):          2,068
Average cycles per product:   20.7
```

---

## 🔢 **Fibonacci Sequence** - Iterative Algorithm

### `fibonacci.txt`
Generates the first 15 Fibonacci numbers (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377).

**Algorithm:**
- Iterative approach with O(n) time complexity
- Stack-based state management
- Uses `ROT`, `DUP`, and `ADD` creatively

**Run it:**
```bash
python3 src/stackc.py examples/fibonacci.txt
python3 src/stackr.py examples/fibonacci.stkm
```

**With Trace (demo version):**
```bash
python3 src/stackc.py examples/fibonacci_demo.txt
python3 src/stackr.py examples/fibonacci_demo.stkm --trace
```

**Performance Analysis:**
```bash
python3 examples/fibonacci_stats.py
```

**Output:**
```
Fibonacci Sequence (First 15) - Performance Analysis
Instructions executed:        215
Total cycles (cost):          300
Average cycles per number:    20.0
Average cost per instruction: 1.40
```

---

## 🎯 **New Features Demo**

### `demo_new_features.txt`
Demonstrates all 9 new opcodes added in the latest update.

**Showcases:**
- Comparison opcodes: `EQ`, `NEQ`, `LT`, `GT`, `LTE`, `GTE`
- Stack introspection: `DEPTH`, `OVER`, `ROT`

**Run it:**
```bash
python3 src/stackc.py examples/demo_new_features.txt
python3 src/stackr.py examples/demo_new_features.stkm
```

---

## 💡 **Cost Tracking Demo**

### `test_cost_tracking.py`
Shows how instruction costs work (multiplication costs 3× more than addition).

**Run it:**
```bash
python3 examples/test_cost_tracking.py
```

---

## ❌ **Error Suggestion Demo**

### `test_error_suggestion.txt`
Demonstrates improved error messages with fuzzy matching.

**Example:**
```bash
python3 src/stackc.py examples/test_error_suggestion.txt
# Output: Line 4: Unknown opcode 'AD' (did you mean ADD?)
```

---

## 📚 **Learning Path**

1. **Start here:** `demo_new_features.txt` - See all opcodes in action
2. **Simple algorithm:** `fibonacci.txt` - Iterative loop with state management
3. **Nested loops:** `times_tables.txt` - More complex control flow
4. **Performance:** `*_stats.py` files - Understand instruction costs

---

## 🔧 **Useful Commands**

**Compile and run:**
```bash
python3 src/stackc.py examples/program.txt
python3 src/stackr.py examples/program.stkm
```

**With trace (see execution):**
```bash
python3 src/stackr.py examples/program.stkm --trace
```

**With step mode (interactive):**
```bash
python3 src/stackr.py examples/program.stkm --step
```

**Disassemble:**
```bash
python3 src/stackp.py examples/program.stkm
python3 src/stackp.py examples/program.stkm -v  # verbose with hex
```

---

## 📈 **Complexity Comparison**

| Program | Instructions | Cycles | Output Count |
|---------|--------------|--------|--------------|
| Fibonacci (15) | 215 | 300 | 15 |
| Times Tables (100) | 1,237 | 2,068 | 100 |

**Note:** Times tables requires more instructions per output due to nested loop overhead.

---

## 🎓 **Key Concepts Demonstrated**

### Stack Manipulation
- `DUP` - Duplicate top value
- `SWAP` - Swap top two values
- `ROT` - Rotate top three values
- `OVER` - Copy second value to top
- `DEPTH` - Push stack depth

### Control Flow
- `JUMP` - Unconditional jump
- `JZ` - Jump if zero
- Labels (e.g., `LOOP:`) - Named jump targets

### Comparisons
- `EQ` / `NEQ` - Equality tests
- `LT` / `GT` - Less/greater than
- `LTE` / `GTE` - Less/greater or equal

### Performance
- Instruction cost tracking
- Weighted cycles (DIV=10, MUL=3, ADD=1)
- Educational tool for understanding algorithm efficiency

---

**Happy coding with Stack Machine! 🚀**
