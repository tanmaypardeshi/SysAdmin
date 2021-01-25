#!/bin/bash

echo "Setting up SysAdmin Executable"
pyinstaller main.py --onefile --name SysAdmin --paths venv/lib/python3.8/site-packages --paths scripts --key="4Gk5vJbyN4wC7wK7C"
pyinstaller SysAdmin.spec
echo "Done"
