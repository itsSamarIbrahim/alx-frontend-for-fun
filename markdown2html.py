#!/usr/bin/python3
"""
A python script to convert markdown files to HTML files.
"""
import sys
import os


if len(sys.argv) < 3:
    """nn"""
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    sys.exit(1)

input_file = sys.argv[1]
if not os.path.exists(input_file):
    """mmm"""
    sys.stderr.write(f"Missing {input_file}\n")
    sys.exit(1)

sys.exit(0)
