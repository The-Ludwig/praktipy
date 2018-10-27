#!/bin/bash
echo $(dirname "$(pwd)")
if ! [[ $PYTHONPATH == *$(dirname "$(pwd)")* ]]; then
	if [ -f tablehandler.py ]; then
		echo "Adding praktipy package to PYTHONPATH"
		export PYTHONPATH=$PYTHONPATH:$(dirname "$(pwd)")
		echo "export PYTHONPATH=\$PYTHONPATH:$(dirname "$(pwd)")" >> ~/.bashrc
	else 
		echo "Please execute the install script in imports/praktipy"
	fi
else
	echo "Praktipy allready seems to be installed (in your PYTHONPATH)"
	echo "Won't install anything"
fi
