#!/bin/sh

cd "$(dirname "$0")"
cd ..
python manage.py test
cd -
convert -density 300 gameboard.svg gameboard.pdf
pdfposter -m a4 -p a2 gameboard.pdf gameboard_split.pdf
