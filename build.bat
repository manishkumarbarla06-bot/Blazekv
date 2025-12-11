@echo off
REM BlazeKV Build Script for Windows
REM This script compiles BlazeKV using available C compilers

echo Building BlazeKV...

REM Try GCC first
where gcc >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Compiling with GCC...
    gcc -Wall -Wextra -O2 blazekv.c -o blazekv.exe
    if %ERRORLEVEL% == 0 (
        echo Build successful! Run with: blazekv.exe
    ) else (
        echo Build failed!
        exit /b 1
    )
    goto :eof
)

REM Try MSVC
where cl >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Compiling with MSVC...
    cl /O2 blazekv.c /Fe:blazekv.exe
    if %ERRORLEVEL% == 0 (
        echo Build successful! Run with: blazekv.exe
    ) else (
        echo Build failed!
        exit /b 1
    )
    goto :eof
)

REM Try MinGW
where mingw32-gcc >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Compiling with MinGW...
    mingw32-gcc -Wall -Wextra -O2 blazekv.c -o blazekv.exe
    if %ERRORLEVEL% == 0 (
        echo Build successful! Run with: blazekv.exe
    ) else (
        echo Build failed!
        exit /b 1
    )
    goto :eof
)

echo Error: No C compiler found in PATH!
echo Please install GCC, MSVC, or MinGW
exit /b 1
