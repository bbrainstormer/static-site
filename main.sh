#! /bin/bash

python3 src/generate_content.py
python3 src/main.py
cd public && python3 -m http.server 8888
