#!/usr/bin/env python3
import sys
import dbus

servernum = '1'
minusers = 0
maxusers = 0
minchannels = 0
maxchannels = 0
minbans = 0
maxbans = -1
warning = False
reportstr = ""
warningstr = ""

if(len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help'):
	print('usage: ' + sys.argv[0] + ' <server number> <minusers> <maxusers> <minchannels> <maxchannels> <minbans> <maxbans>')
	print('minimus: <= 0: disabled (except maxbans, only disabled for <= -1); maximums: <= 0 disabled; server numbers start with 1!')
	sys.exit()

servernum = sys.argv[1]
if(int(sys.argv[2]) > 0):
	minusers = int(sys.argv[2])
if(int(sys.argv[3]) > 0):
	maxusers = int(sys.argv[3])
if(int(sys.argv[4]) > 0):
	minchannels = int(sys.argv[4])
if(int(sys.argv[5]) > 0):
	maxchannels = int(sys.argv[5])
if(int(sys.argv[6]) > 0):
	minbans = int(sys.argv[6])
if(int(sys.argv[7]) > -1):
	maxbans = int(sys.argv[7])

bus = dbus.SystemBus()
server = bus.get_object('net.sourceforge.mumble.murmur', '/'+str(servernum))
try:
	players = server.getPlayers()
except dbus.exceptions.DBusException:
	print("Critical: No connection via dbus. If dbus is up this service is probably down.")
	sys.exit(2) #Crit
channels = server.getChannels()
bans = server.getBans()

reportstr += "users: " + str(len(players)) + ", channels: " + str(len(channels)) + ", bans: " + str(len(bans))

if(minusers > 0):
	if(minusers > len(players)):
		warning = True
		warningstr += " <less than " + str(minusers) + " users>"
if(maxusers > 0):
	if(maxusers < len(players)):
		warning = True
		warningstr += " <more than " + str(maxusers) + " users>"
if(minchannels > 0):
	if(minchannels > len(channels)):
		warning = True
		warningstr += " <less than " + str(minchannels) + " channels>"
if(maxchannels > 0):
	if(maxchannels < len(channels)):
		warning = True
		warningstr += " <more than " + str(maxchannels) + " channels>"
if(minbans > 0):
	if(minbans > len(bans)):
		warning = True
		warningstr += " <less than " + str(minbans) + " bans>"
if(maxbans > -1):
	if(maxbans < len(bans)):
		warning = True
		warningstr +=" <more than " + str(maxbans) + " bans>"

if(warning):
	reportstr = "WARNING: " + reportstr + ", warnings:" + warningstr
else:
	reportstr = "OK: " + reportstr
print(reportstr)
if(warning):
	sys.exit(1)
else:
	sys.exit()
