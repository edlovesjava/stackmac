#!/bin/bash
# Demo script to show banner functionality

echo "========================================"
echo "BANNER DEMO - Stack Machine Tools"
echo "========================================"
echo

echo "1. Testing stackc with banner suppressed:"
echo "   python3 stackc.py example1_arithmetic.txt --no-banner"
python3 stackc.py example1_arithmetic.txt --no-banner
echo

echo "========================================"
echo "2. Testing stackr with banner suppressed:"
echo "   python3 stackr.py example1_arithmetic.stkm --no-banner"
python3 stackr.py example1_arithmetic.stkm --no-banner
echo

echo "========================================"
echo "3. Testing stackp (stdout - no banner by default):"
echo "   python3 stackp.py example1_arithmetic.stkm | head -5"
python3 stackp.py example1_arithmetic.stkm | head -5
echo

echo "========================================"
echo "4. Testing stackp with -v (banner should show in TTY):"
echo "   python3 stackp.py example1_arithmetic.stkm -v --no-banner | head -5"
python3 stackp.py example1_arithmetic.stkm -v --no-banner | head -5
echo

echo "========================================"
echo "5. Environment variable test:"
echo "   export STACKMAC_NO_BANNER=1"
export STACKMAC_NO_BANNER=1
echo "   python3 stackc.py example1_arithmetic.txt"
python3 stackc.py example1_arithmetic.txt
echo

echo "========================================"
echo "Demo complete!"
echo "========================================"
