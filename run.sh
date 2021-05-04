#!/bin/bash



DIR=~/.config/cmus/scripts/cmus_notify/
cd $DIR
source venv/bin/activate
$DIR/songChange.py -l -s

