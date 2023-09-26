#!/usr/bin/python3

import telnetlib
from datetime import datetime
import MySQLdb

HOST = "127.0.0.1"
loginDict = {}

telnet = telnetlib.Telnet(HOST, "7505", 5)
telnet.write("status\n".encode("ascii"))
outputUDP = telnet.read_until("END\n".encode('utf-8'), 1).decode('ascii').split("\n")
telnet.close()

for string in outputUDP:
    if len(string.split(",")) == 5:
        if "Common Name" not in string:
            login = string.split(",")[0]
            ts = datetime.strptime(string.split(",")[-1].strip(), '%a %b %d %H:%M:%S %Y').timestamp()
            loginDict[login] = ts

telnet = telnetlib.Telnet(HOST, "7506", 5)
telnet.write("status\n".encode("ascii"))
outputTCP = telnet.read_until("END\n".encode('utf-8'), 1).decode('ascii').split("\n")
telnet.close()

for string in outputTCP:
    if len(string.split(",")) == 5:
        if "Common Name" not in string:
            login = string.split(",")[0]
            ts = datetime.strptime(string.split(",")[-1].strip(), '%a %b %d %H:%M:%S %Y').timestamp()
            loginDict[login] = ts

db = MySQLdb.connect(host='localhost', user='ovpn', passwd='ovpnPass', db='ovpn', charset="utf8")
cursor = db.cursor()

for login in loginDict:
    if login == "UNDEF": continue # ignore shit connects
    # Fetch last login for user
    cursor.execute("SELECT id, login, since, datetime FROM stats WHERE login = '%s' ORDER BY id DESC LIMIT 1" % login)
    result = cursor.fetchall()
    # If user not found, write him to db
    if len(result) == 0:
        cursor.execute("INSERT INTO stats(login, since) values ('%s', '%s')" % (login, loginDict[login]))
        db.commit()
    else:
        for row in result:
            # If since NOT as old, creating new row
            if str(loginDict[login]) != row[2]:
                cursor.execute("INSERT INTO stats(login, since) values ('%s', '%s')" % (login, loginDict[login]))
                db.commit()
            # Just update datetime as current
            else:
                cursor.execute("UPDATE stats SET datetime = CURRENT_TIMESTAMP() WHERE id = '%s'" % row[0])
                db.commit()

cursor.close()
db.close()
