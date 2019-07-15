# Installs the assistant located at the first parameter
# How to call this script: 
# /home/pi/synthia/_snips_install.sh /home/pi/Downloads/<assistant>.zip
# Where <assistant>.zip is the zip filename downloaded from snips.ai after training your assistant

if [ -z "$1" ]
  then
    echo "No assistant zip file passed in argument 1"
    exit 1
fi

# Install assistant
sudo rm -rf /usr/share/snips/assistant/
sudo mkdir /usr/share/snips
sudo unzip $1 -d /usr/share/snips/
snips-template render
sudo systemctl restart 'snips-*'
