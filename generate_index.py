#!/usr/bin/env python
"""
generate index.html
"""

import generate_gameboard
import generate_resource_wheel

def main():
    """
    generate index.html
    """
    generate_gameboard.main()
    generate_resource_wheel.main()

    with open("index.html", 'w') as out_file:
        with open("top_of_index.txt", 'r') as in_file:
            out_file.write(in_file.read())
        with open("gameboard.svg", 'r') as in_file:
            out_file.write(in_file.read())
        with open("wheel.svg", 'r') as in_file:
            out_file.write(in_file.read())
        with open("bottom_of_index.txt", 'r') as in_file:
            out_file.write(in_file.read())

if __name__ == '__main__':
    main()
