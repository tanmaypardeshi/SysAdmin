#!/bin/bash

read -p "Enter email:- " EMAIL

if [ -z "$EMAIL" ] 
then
	echo "Email cannot be empty"
	echo "Exiting...."
	exit 1
fi

echo "Setting up SysAdmin Executable"
pyinstaller main.py --onefile --name SysAdmin --paths venv/lib/python3.8/site-packages --paths scripts  --key="4Gk5vJbyN4wC7wK7C"
echo "Done"

filename2="email.txt"
touch $filename2

echo "$EMAIL" >> $filename2

sudo mv $filename2 /home/tanmay/SysAdmin
