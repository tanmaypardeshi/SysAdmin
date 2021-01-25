#!/bin/bash

read -p "Enter email:- " EMAIL

if [ -z "$EMAIL" ] 
then
	echo "Email cannot be empty"
	echo "Exiting...."
	exit 1
fi

if [ -e CDFN-client ]
then
	sudo cp CDFN-client /home/$USER/CDFN/
else
	echo "CDFN-client not found. Make sure it is in the same directory as install.sh"
	echo "Exiting...."
	exit 1
fi

sudo cd /home/$USER/SysAdmin/

./SysAdmin