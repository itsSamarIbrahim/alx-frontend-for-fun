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
        in_list = False # flag to check if we are inside an unordered list

        for line in lines:
            stripped_line = line.strip()

            # check for headings
            if stripped_line.startswith("#"):
                # count the number of '#' at the start
                heading_level = len(stripped_line.split()[0])
                if 1 <= heading_level <= 6:
                    heading_text = stripped_line[heading_level:].strip()
                    html_content += f"<h{heading_level}>{heading_text}</h{heading_level}>\n"

                #if a heading is found and we are in a list, close the list
                if in_list:
                    html_content += "</ul>\n"
                    in_list = False

            #check for list items
            elif stripped_line.startswith("- "):
                if not in_list:
                    html_content += "<ul>\n"
                    in_list = True
                list_item = stripped_line[2:].strip()
                html_content += f"  <li>{list_item}</li>\n"

            else:
                # if we encounter a non-list and non-heading line, we are in a list, close the list
                if in_list:
                    html_content += "</ul>\n"
                    in_list = False

        # if the file ends while still inside a list, close the list
        if in_list:
            html_content += "</ul>\n"
        
        # write the html content to the html_file
        with open(html_file, 'w') as html:
            html.write(html_content)

except Exception as e:
    sys.stderr.write(f"Error: {e}\n")
    sys.exit(1)


# if all is good, exit with code 0
sys.exit(0)
