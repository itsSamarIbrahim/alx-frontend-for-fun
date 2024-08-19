#!/usr/bin/env python3
import sys
import os


# check the number of args
if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    sys.exit(1)

# check id the markdown file exists
md_file = sys.argv[1]
html_file = sys.argv[2]

if not os.path.exists(md_file):
    sys.stderr.write(f"Missing {md_file}\n")
    sys.exit(1)

# read the markdown file and parse headings
try:
    with open(md_file, 'r') as md:
        lines = md.readlines()

        # convert markdown to html
        html_content = ""
        in_unordered_list = False # flag to check if we are inside an unordered list
        in_ordered_list = False # flag to check if we are inside an ordered list
        in_paragraph = False # flag to check if we are inside a paragraph
        current_paragraph = ""

        for line in lines:
            stripped_line = line.strip()

            # check for headings
            if stripped_line.startswith("#"):
                # count the number of '#' at the start
                heading_level = len(stripped_line.split()[0])
                if 1 <= heading_level <= 6:
                    heading_text = stripped_line[heading_level:].strip()
                    html_content += f"<h{heading_level}>{heading_text}</h{heading_level}>\n"

                # close any open list or paragraph before processing a heading
                if in_unordered_list:
                    html_content += "</ul>\n"
                    in_unordered_list = False

                if in_ordered_list:
                    html_content += "</ol>\n"
                    in_ordered_list = False

                if in_paragraph:
                    lines_in_paragraph = "\n\t<br />\n\t".join(current_paragraph.split("\n"))
                    html_content += f"<p>\n\t{lines_in_paragraph}\n</p>\n"
                    in_paragraph = False
                    current_paragraph = ""

            #check for unordered list items
            elif stripped_line.startswith("- "):
                if not in_unordered_list:
                    if in_ordered_list: # close ordered list if open
                        html_content += "</ol>\n"
                        in_ordered_list = False
                    if in_paragraph: # closr paragraph if open
                        lines_in_paragraph = "\n\t<br />\n\t".join(current_paragraph.split("\n"))
                        html_content += f"<p>\n\t{lines_in_paragraph}\n</p>\n"
                        in_paragraph = False
                        current_paragraph = ""
                    html_content += "<ul>\n"
                    in_unordered_list = True
                list_item = stripped_line[2:].strip()
                html_content += f"  <li>{list_item}</li>\n"

            # check for ordered list items
            elif stripped_line.startswith("* "):
                if not in_ordered_list:
                    if in_unordered_list: # close unordered list if open
                        html_content += "</ul>\n"
                        in_unordered_list = False
                    if in_paragraph: # close paragraph
                        lines_in_paragraph = "\n\t<br />\n\t".join(current_paragraph.split("\n"))
                        html_content += f"<p>\n\t{lines_in_paragraph}\n</p>\n"
                        in_paragraph = False
                        current_paragraph = ""
                    html_content += "<ol>\n"
                    in_ordered_list = True
                list_item = stripped_line[2:].strip()
                html_content += f"  <li>{list_item}</li>\n"

            # check for paragraph text
            else:
                if stripped_line: # non-empty line
                    if not in_paragraph:
                    # if we encounter a non-list and non-heading line, we are in a list, close the list
                        if in_unordered_list:
                            html_content += "</ul>\n"
                            in_unordered_list = False
                        if in_ordered_list:
                            html_content += "</ol>\n"
                            in_ordered_list = False
                        in_paragraph = True
                        current_paragraph = stripped_line
                    else:
                        current_paragraph += f"\n{stripped_line}"
                else: # empty line indicates the end of a paragraph
                    if in_paragraph:
                        # split the paragraph text into lines and indent each line
                        lines_in_paragraph = "\n\t<br />\n\t".join(current_paragraph.split("\n"))
                        html_content += f"<p>\n\t{lines_in_paragraph}\n</p>\n"
                        in_paragraph = False
                        current_paragraph = "" 

        # close any remaining open lists or paragraphs at the end of the file
        if in_unordered_list:
            html_content += "</ul>\n"
        if in_ordered_list:
            html_content += "</ol>\n"
        if in_paragraph:
            lines_in_paragraph = "\n\t<br />\n\t".join(current_paragraph.split("\n"))
            html_content += f"<p>\n\t{lines_in_paragraph}\n</p>\n"

        # write the html content to the html_file
        with open(html_file, 'w') as html:
            html.write(html_content)

except Exception as e:
    sys.stderr.write(f"Error: {e}\n")
    sys.exit(1)


# if all is good, exit with code 0
sys.exit(0)
