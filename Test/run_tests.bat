@echo off
echo ========================================
echo HackRX API v2 Test Scripts
echo ========================================
echo.
echo Available test options:
echo.
echo 1. Simple Test    - Basic API v2 test
echo 2. Load Test      - Comprehensive testing with options
echo 3. Load Test + Verbose - Detailed output
echo 4. Repeat Test    - Run test multiple times
echo 5. Custom Server - Test different server
echo.
set /p choice="Choose option (1-5): "

if "%choice%"=="1" (
    echo.
    echo Running simple test...
    python Test\simple_test.py
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Running load test...
    python Test\load_test.py
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Running load test with verbose output...
    python Test\load_test.py --verbose
    goto end
)

if "%choice%"=="4" (
    echo.
    set /p repeats="Number of repeats (default 3): "
    if "%repeats%"=="" set repeats=3
    echo Running load test %repeats% times...
    python Test\load_test.py --repeat %repeats%
    goto end
)

if "%choice%"=="5" (
    echo.
    set /p server="Server URL (default http://localhost:8000): "
    if "%server%"=="" set server=http://localhost:8000
    echo Testing server: %server%
    python Test\load_test.py --server %server% --verbose
    goto end
)

echo Invalid choice. Please run the script again.

:end
echo.
echo ========================================
echo Test completed. Press any key to exit.
pause >nul
