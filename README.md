# ovpnstats-flask
This app collect statistic from openvpn connects and show it via flask as webpage.

## Preparation
### Need:
- Linux server(Ubuntu) with user with sudo privilage.
- Nginx installed.
- Domain name(optional).
```
git clone https://github.com/vansatchen/ovpnstats-flask.git
```
### Installations:
```
$ sudo apt update
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```
Make virtual environment(optional)
```
$ sudo apt install python3-venv
$ cd ./ovpnstats-flask
$ python3 -m venv venv
# Activate virtual environment
$ source venv/bin/activate
```
Install nedded python modules from pip
```
$ pip install wheel
```
> In venv use **pip**, not pip3
```
$ pip install uwsgi flask flask-sqlalchemy mysqlclient python-ldap
```
