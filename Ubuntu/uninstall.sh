#!/bin/bash

echo ""
echo "Stopping supervisor..."
sudo service supervisor stop
sudo apt-get remove supervisor
echo "Stopped supervisor"

echo ""
echo "Clearing files and config..."
sudo rm -rf /usr/SysAdmin /etc/supervisor/conf.d/SysAdmin.conf
echo "Remved config and files"

echo ""
echo "Stopping the service..."
sudo pkill -f SysAdmin
echo "Stopped service"

echo ""
echo "Uninstalled successfully"



