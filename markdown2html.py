#!/usr/bin/python3
"""
A python script to convert markdown files to HTML files.
"""
import sys
import os
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    md_file, html_file = sys.argv[1], sys.argv[2]

    if not os.path.exists(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    def convert_bold_and_italic(line):
        """Converts bold (**text**) and italic (__text__) markdown to HTML."""
        line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
        line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)
        return line

    def replace_md5(line):
        """Replaces [[text]] with its MD5 hash."""
        md5_pattern = re.findall(r'\[\[(.*?)\]\]', line)
        for match in md5_pattern:
            line = line.replace(f'[[{match}]]',
                                hashlib.md5(match.encode()).hexdigest())
        return line

    def remove_c(line):
        """Removes all 'c' and 'C' characters
        from text enclosed in ((text))."""
        c_pattern = re.findall(r'\(\((.*?)\)\)', line)
        for match in c_pattern:
            line = line.replace(f'(({match}))',
                                match.replace('c', '').replace('C', ''))
        return line

    with open(md_file, 'r') as md, open(html_file, 'w') as html:
        unordered_start, ordered_start, paragraph = False, False, False

        for line in md:
            line = line.strip()
            line = convert_bold_and_italic(line)
            line = replace_md5(line)
            line = remove_c(line)

            # Handle headings
            heading_level = len(line) - len(line.lstrip('#'))
            if 1 <= heading_level <= 6:
                html.write(f"<h{heading_level}>{line[heading_level:].strip()}\
                           </h{heading_level}>\n")
                unordered_start = ordered_start = paragraph = False

            # Handle unordered lists
            elif line.startswith("- "):
                if not unordered_start:
                    if ordered_start:
                        html.write("</ol>\n")
                        ordered_start = False
                    html.write("<ul>\n")
                    unordered_start = True
                html.write(f"  <li>{line[2:].strip()}</li>\n")
                paragraph = False

            # Handle ordered lists
            elif line.startswith("* "):
                if not ordered_start:
                    if unordered_start:
                        html.write("</ul>\n")
                        unordered_start = False
                    html.write("<ol>\n")
                    ordered_start = True
                html.write(f"  <li>{line[2:].strip()}</li>\n")
                paragraph = False

            # Handle paragraphs
            elif line:
                if not paragraph:
                    if unordered_start:
                        html.write("</ul>\n")
                        unordered_start = False
                    if ordered_start:
                        html.write("</ol>\n")
                        ordered_start = False
                    html.write("<p>\n")
                    paragraph = True
                html.write(f"  {line}\n")
            else:
                if paragraph:
                    html.write("</p>\n")
                    paragraph = False

        # Close any remaining open tags
        if unordered_start:
            html.write("</ul>\n")
        if ordered_start:
            html.write("</ol>\n")
        if paragraph:
            html.write("</p>\n")

    sys.exit(0)
