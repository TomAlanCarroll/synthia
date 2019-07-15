# Installs the assistant located at the first parameter
# How to call this script: 
# /home/pi/synthia/snips_skills_install.sh <owm-api-key> <owm-location>
# Where <owm-api-key> is your API key found on https://home.openweathermap.org/api_keys after signing up
# Where <owm-location> is your location, example city or zip code: 'New York' or 10001


if [ -z "$1" ]
  then
    echo "No Open Weather Map API key passed in argument 2, see https://home.openweathermap.org/api_keys"
    exit 1
fi
if [ -z "$2" ]
  then
    echo "No Open Weather Map location passed in argument 3, try 'New York' or 10001"
    exit 1
fi

cd /var/lib/snips/skills

# Skill openweathermap install
git clone https://github.com/snipsco/snips-skill-owm.git /var/lib/snips/skills/snips-skill-owm
cd /var/lib/snips/skills/snips-skill-owm
echo "[global]

[secret]
api_key=$1
locale=en_US
default_location=$2
" | tee -a /var/lib/snips/skills/snips-skill-owm/config.ini
virtualenv --no-site-packages venv
source /var/lib/snips/skills/snips-skill-owm/venv/bin/activate
sh setup.sh
deactivate

