#!/bin/bash

read -p "Enter email:- " EMAIL

if [ -z "$EMAIL" ] 
then
	echo "Email cannot be empty"
	echo "Exiting...."
	exit 1
fi

sudo mkdir /home/$USER/SysAdmin/

filename1="email.txt"

touch $filename1

echo "$EMAIL" >> $filename1

sudo mv $filename1 /home/$USER/SysAdmin/

if [ -e SysAdmin ]
then
	sudo cp SysAdmin /home/$USER/SysAdmin/
else
	echo "SysAdmin not found. Make sure it is in the same directory as install.sh"
	echo "Exiting...."
	exit 1
fi

cd /home/$USER/SysAdmin/

./SysAdmin