#!/bin/bash

read -p "Enter email:- " EMAIL

if [ -z "$EMAIL" ] 
then
	echo "Email cannot be empty"
	echo "Exiting...."
	exit 1
fi

echo "Installing packages..."
echo ""
echo "Installing supervisor"
sudo apt-get install supervisor -qq -y
echo "Installed supervisor successfully"
echo "Building script to run executable..."

sudo mkdir -p /usr/SysAdmin/

if [ -e SysAdmin ]
then
	sudo cp SysAdmin /usr/SysAdmin/
else
	echo "SysAdmin not found. Make sure it is in the same directory as install.sh"
	echo "Exiting...."
	exit 1
fi

filename="email.txt"
touch $filename

echo "$EMAIL" >> $filename

sudo mv $filename /usr/SysAdmin/

filename1="run.sh"
touch $filename1

echo "#!/bin/bash" >> $filename1
echo "cd /usr/SysAdmin/" >> $filename1
echo "./SysAdmin" >> $filename1
echo "exit 0" >> $filename1

sudo mv $filename1 /usr/SysAdmin/
sudo chmod +x /usr/SysAdmin/$filename1

echo ""
echo "Script built"

echo ""
echo "Creating conf file..."

sudo mkdir -p /var/log/SysAdmin

filename2="SysAdmin.conf"
touch $filename2

echo "[program:SysAdmin]" >> $filename2
echo "directory=/usr/SysAdmin" >> $filename2
echo "command=/usr/SysAdmin/run.sh" >> $filename2
echo "autostart=true" >> $filename2
echo "autorestart=true" >> $filename2
echo "stderr_logfile=/var/log/SysAdmin/SysAdmin.err.log" >> $filename2
echo "stdout_logfile=/var/log/SysAdmin/SysAdmin.out.log" >> $filename2

sudo mv $filename2 /etc/supervisor/conf.d/
sudo service supervisor start
sudo supervisorctl update
echo ""
echo "Conf file running"

echo ""
echo "Client ready and running as a service"
exit 0
