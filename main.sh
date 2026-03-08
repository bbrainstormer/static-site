#! /bin/bash

python3 generate_public.py
python3 src/main.py
cd public && python3 -m http.server 8888
