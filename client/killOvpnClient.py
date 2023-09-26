#!/usr/bin/python3

# Use this script to kill ovpn connects per day at 23:59 for correct data connects

import telnetlib
import time

time.sleep(30)

HOST = "127.0.0.1"
loginDict = []

telnet = telnetlib.Telnet(HOST, "7505", 5)
telnet.write("status\n".encode("ascii"))
outputUDP = telnet.read_until("END\n".encode('utf-8'), 1).decode('ascii').split("\n")

for string in outputUDP:
    if len(string.split(",")) == 5:
        if "Common Name" not in string:
            login = string.split(",")[0]
            killString = "kill " + login + "\n"
            telnet.write(killString.encode("ascii"))            

telnet.close()

loginDict = []

telnet = telnetlib.Telnet(HOST, "7506", 5)
telnet.write("status\n".encode("ascii"))
outputTCP = telnet.read_until("END\n".encode('utf-8'), 1).decode('ascii').split("\n")

for string in outputTCP:
    if len(string.split(",")) == 5:
        if "Common Name" not in string:
            login = string.split(",")[0]
            killString = "kill " + login + "\n"
            telnet.write(killString.encode("ascii"))

telnet.close()
