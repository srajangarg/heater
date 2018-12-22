import subprocess
from operator import itemgetter

def toggle_plug():
	print subprocess.check_output(["node",  "js_execs/toggle.js"])
	return

def is_plug_on():
	# output = subprocess.check_output(["node", "js_execs/get_status.js"])
	# if "1" in output:
	# 	return True
	return False

def get_crons():
	disabled, enabled = [], []

	output = subprocess.check_output(["crontab", "-l"])
	for l in output.splitlines():
		if "js_exec" in l:
			words = l.split()

			cur_list = enabled
			if words[0] == "#":
				words = words[1:]
				cur_list = disabled

			cur_list.append([words[1], words[0], "ON" if "turn_on" in words[6] else "OFF"])

	disabled = sorted(disabled, key=itemgetter(0,1))
	enabled = sorted(enabled, key=itemgetter(0,1))

	return disabled, enabled

def delete(hr, min):
	regex = "'%s.*%s'" % (min, hr)
	cmd = "crontab -l | grep 'js_exec' | grep -v " + regex + " | crontab -"
	subprocess.check_output(cmd, shell=True)

def add(hr, min, action, disabled=False):
	hr = str(hr).zfill(2)
	min = str(min).zfill(2)

	new_cron = "%s %s * * * node $PWD/js_execs/" % (min, hr) 
	new_cron += ("turn_on.js" if action == "ON" else "turn_off.js")
	if disabled:
		new_cron = "# " + new_cron

	cmd = '(crontab -l ; echo "' + new_cron + '") | crontab -'
	subprocess.check_output(cmd, shell=True)

def disable(hr, min, action):
	delete(hr, min)
	add(hr, min, action, True)

def enable(hr, min, action):
	delete(hr, min)
	add(hr, min, action)