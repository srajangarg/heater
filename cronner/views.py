# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from helper import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta, time


plug_on = is_plug_on()
last_updated_status = datetime.now()

def index(request):
 	global plug_on, last_updated_status
	
	if (datetime.now() - last_updated_status > timedelta(seconds=60)):
		plug_on = is_plug_on()	
		last_updated_status = datetime.now()

	disabled, enabled = get_crons()

	if plug_on:
		plug_vars = ["ON", "red", "teal", "OFF"]
	else:
		plug_vars = ["OFF", "teal", "red", "ON"]

	return render(request, "board.html", {
											"finalList": [[0, 1, 2, 3]], 
											"plug_vars" : plug_vars,
											"last_updated_status" : last_updated_status.strftime("%I:%M:%S %p"),
											"enabled" : enabled,
											"disabled": disabled
										})

def toggle(request):

	global plug_on, last_updated_status
	toggle_plug()

	plug_on = not plug_on
	last_updated_status = datetime.now()
	return redirect("/cronner")

def add_cron(request):

	disabled, enabled = get_crons()
	total = disabled + enabled

	time_list = [":".join(x[:2]) for x in total]

	start_time = datetime.strptime(request.POST.get("time"), "%H:%M")
	repeat_time = datetime.strptime(request.POST.get("repeat_time"), "%H:%M")
	repeat_offset = timedelta(hours=repeat_time.hour, minutes=repeat_time.minute)

	to_add = []
	for i in xrange(int(request.POST.get("num_repeat"))):
		to_add.append(start_time + i*repeat_offset)

	for time in to_add:
		if time.strftime("%H:%M") not in time_list:
			add(str(time.hour), str(time.minute), request.POST.get("action"))

	return redirect("/cronner")

def delete_cron(request):

	hr = request.GET.get("hr")
	min = request.GET.get("min")

	if hr and min:
		delete(hr, min)		

	return redirect("/cronner")

def disable_cron(request):

	hr = request.GET.get("hr")
	min = request.GET.get("min")
	action = request.GET.get("action")

	if hr and min and action:
		disable(hr, min, action)		

	return redirect("/cronner")

def enable_cron(request):

	hr = request.GET.get("hr")
	min = request.GET.get("min")
	action = request.GET.get("action")

	if hr and min and action:
		enable(hr, min, action)		

	return redirect("/cronner")
