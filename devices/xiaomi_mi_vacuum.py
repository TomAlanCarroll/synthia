import config
from subprocess import check_call

'''
Calls mirobo to control Xiaomi Mi Robot Vacuum. 
MIROBO_IP and MIROBO_TOKEN environment variables must be setup before calling.
For setup see https://github.com/rytilahti/python-mirobo
'''

def clean():
	check_call(['mirobo', 'start'])

def return_to_dock():
	check_call(['mirobo', 'home'])

def set_fanspeed(speed):
	check_call(['mirobo', 'fanspeed', str(speed)])

def set_fanspeed_low():
	set_fanspeed(30)

def set_fanspeed_medium():
	set_fanspeed(50)

def set_fanspeed_high():
	set_fanspeed(80)

def set_fanspeed_max():
	set_fanspeed(100)