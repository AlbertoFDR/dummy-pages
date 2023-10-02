#!/bin/bash

# If you change this port, change also the html's
PORT=1234
DIRECTORY="./"

# Run another process to simulate another origin
python3 -m http.server $PORT --directory $DIRECTORY
