#!/bin/bash
# BlazeKV Build Script for Linux/macOS

echo "Building BlazeKV..."

gcc -Wall -Wextra -O2 blazekv.c -o blazekv

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "Run with: ./blazekv"
else
    echo "❌ Build failed!"
    exit 1
fi
