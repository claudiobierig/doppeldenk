#!/usr/bin/env python
"""
generate index.html
"""

import os
from . import generate_gameboard
from . import generate_resource_wheel
from . import generate_player_board

def main():
    """
    generate index.html
    """
    generate_gameboard.main()
    #generate_player_board.main()
    #generate_resource_wheel.main()
    current_directory = os.path.dirname(os.path.abspath(__file__))
    files = ["top_of_index.txt", "../gameboard.svg", #"playerboard.svg", "wheel.svg",
             "bottom_of_index.txt"]
    write_file = "/home/claudio/shared/workspace/doppeldenk/django/doppeldenk/spacetrading/templates/spacetrading/game_detail.html"
    with open(write_file, 'w') as out_file:
        for file_name in files:
            with open(os.path.join(current_directory, file_name), 'r') as in_file:
                out_file.write(in_file.read())

if __name__ == '__main__':
    main()
