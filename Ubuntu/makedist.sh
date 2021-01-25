#!/bin/bash

echo "Setting up SysAdmin Executable"
pyinstaller main.py --onefile --name SysAdmin --paths venv/lib/python3.8/site-packages --paths scripts --add-data "credentials.json:." --add-data "token.pickle:." --key="4Gk5vJbyN4wC7wK7C"
echo "Done"
