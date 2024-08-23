#!/usr/bin/python3
"""
A python script to convert markdown files to HTML files.
"""
import sys
import os


# Step 1: Check the number of arguments
if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    sys.exit(1)

# Step 2: Check if the Markdown file exists
input_file = sys.argv[1]
if not os.path.exists(input_file):
    sys.stderr.write(f"Missing {input_file}\n")
    sys.exit(1)

# Step 3: If everything is fine, exit with code 0
sys.exit(0)
