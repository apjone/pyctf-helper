#!/bin/bash
export FLASK_APP=pp42
export FLASK_ENV=development
#static/winPEAS.bat
if [  ! `find static -type f -mtime -7 -name linpeas.sh` ] ; then 
	while [[ "$linupdate" != "n" && "$linupdate" != "y" ]]
	do
		read -p "LinPeas is older than 7 days or does not exist, update LinPeas? [y/n]: " linupdate
	done
	if [ "$linupdate" = "y" ]; then
		wget https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh -O static/linpeas.sh
	fi
fi

if [ ! `find static -type f -mtime -7 -name winPEAS.bat` ] ; then 
	while [[ "$winupdate" != "n" && "$winupdate" != "y" ]]
	do
		read -p "WinPeas is older than 7 days or does not exist, update WinPeas? [y/n]: " winupdate
	done
	if [ "$winupdate" = "y" ]; then
		wget https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/winPEAS/winPEASbat/winPEAS.bat -O static/winPEAS.bat
	fi
fi

flask run --host=0.0.0.0 --port=9999
