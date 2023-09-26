from flask import Flask, redirect, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from datetime import datetime, timedelta
import time
import ldapFunc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ovpnUser:ovpnPass@host1/ovpn'
app.config['SQLALCHEMY_BINDS'] = {
    'ovpn1': 'mysql://ovpnUser:ovpnPass@host1/ovpn',
    'ovpn2': 'mysql://ovpnUser:ovpnPass@host2/ovpn',
    'ovpn3': 'mysql://ovpnUser:ovpnPass@host3/ovpn'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
timeSleep = 4

class DB1(db.Model):
    __bind_key__ = 'ovpn1'
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40))
    since = db.Column(db.String(40))
    datetime = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<%r>' % self.datetime


db.metadata.clear()


class DB2(db.Model):
    __bind_key__ = 'ovpn2'
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40))
    since = db.Column(db.String(40))
    datetime = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<%r>' % self.datetime


db.metadata.clear()


class DB3(db.Model):
    __bind_key__ = 'ovpn3'
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40))
    since = db.Column(db.String(40))
    datetime = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        return '<%r>' % self.datetime


@app.route('/')
def index():
    defaultPage = '/host1'
    return redirect(defaultPage)


@app.route('/<string:dep>')
def dep(dep):
    fullDateTimeNow = datetime.now()
    datetimeNow = fullDateTimeNow.strftime("%Y-%m-%d %H:%M")
    secondsNow = int(float(fullDateTimeNow.strftime("%S")))
    if 0 <= secondsNow <= timeSleep:
        datetimeNow = fullDateTimeNow - timedelta(seconds=30)
        datetimeNow = datetimeNow.strftime("%Y-%m-%d %H:%M")

    if dep == 'host1':
        ldapGroup = 'ovpn1'
        users = DB1.query.order_by(DB1.id).all()
        ldapResult = ldapFunc.connectionLdap(ldapGroup)
    elif dep == 'host2':
        ldapGroup = 'ovpn2'
        users = DB2.query.order_by(DB2.id).all()
        ldapResult = ldapFunc.connectionLdap(ldapGroup)
    elif dep == 'host3':
        ldapGroup = 'ovpn3'
        users = DB3.query.order_by(DB3.id).all()
        ldapResult = ldapFunc.connectionLdapDB3()
    else:
        return redirect('/')

    q = request.args.get('q')
    if q:
        ldapUser = ldapFunc.getUser(ldapGroup, q)
        if ldapUser: return redirect("/" + dep + "/" + ldapUser[0][0].split(',')[0].split('=')[1])

    conUsers = []
    for ldapUser in ldapResult:
        ldapADLogin = ldapUser[1].get("sAMAccountName")[0].decode("utf-8").replace('$','')
        ldapADCN = ldapUser[0].split(',')[0].split('=')[1]
        for user in users:
            if user.login == ldapADLogin:
                var = user.datetime.strftime("%Y-%m-%d %H:%M")
                if var >= datetimeNow:
                    user.datetime = "connected"
                    user.login = ldapADCN
                    conUsers.append(user)
    return render_template(dep + ".html", users=conUsers)


@app.route('/<string:dep>/all')
def depAll(dep):
    fullDateTimeNow = datetime.now()
    datetimeNow = fullDateTimeNow.strftime("%Y-%m-%d %H:%M")
    secondsNow = int(float(fullDateTimeNow.strftime("%S")))
    if 0 <= secondsNow <= timeSleep:
        datetimeNow = fullDateTimeNow - timedelta(seconds=30)
        datetimeNow = datetimeNow.strftime("%Y-%m-%d %H:%M")

    if dep == 'host1':
        ldapGroup = 'ovpn1'
        users = DB1.query.order_by(DB1.id).all()
        ldapResult = ldapFunc.connectionLdap(ldapGroup)
    elif dep == 'host2':
        ldapGroup = 'ovpn2'
        users = DB2.query.order_by(DB2.id).all()
        ldapResult = ldapFunc.connectionLdap(ldapGroup)
    elif dep == 'hsot3':
        ldapGroup = 'ovpn3'
        users = DB3.query.order_by(DB3.id).all()
        ldapResult = ldapFunc.connectionLdapDB3()
    else:
        return redirect('/')

    q = request.args.get('q')
    if q:
        ldapUser = ldapFunc.getUser(ldapGroup, q)
        if ldapUser: return redirect("/" + dep + "/" + ldapUser[0][0].split(',')[0].split('=')[1])

    ldapADUsers = []
    for ldapADUser in ldapResult:
        ldapADLogin = ldapADUser[1].get("sAMAccountName")[0].decode("utf-8").replace('$','')
        ldapADCN = ldapADUser[0].split(',')[0].split('=')[1]
        ldapADDT = datetime(1970, 1, 1)
        for user in users:
            userDT = datetime(1970, 1, 1)
            if ldapADLogin == user.login:
                if user.datetime > userDT: userDT = user.datetime
                ldapADDT = userDT
        if ldapADDT == datetime(1970, 1, 1):
            ldapADDT = "нет данных"
        elif ldapADDT.strftime("%Y-%m-%d %H:%M") >= str(datetimeNow):
            ldapADDT = "connected"
        ldapADUsers.append([ldapADLogin, ldapADCN, ldapADDT])
    return render_template(dep + "all.html", ldapADUsers=ldapADUsers)


@app.route('/<string:dep>/user/<string:user>')
def depLogin(dep, user):
    fullDateTimeNow = datetime.now()
    datetimeNow = fullDateTimeNow.strftime("%Y-%m-%d %H:%M")
    secondsNow = int(float(fullDateTimeNow.strftime("%S")))
    monthAgo = fullDateTimeNow - timedelta(days=30)
    if 0 <= secondsNow <= timeSleep:
        datetimeNow = fullDateTimeNow - timedelta(seconds=30)
        datetimeNow = datetimeNow.strftime("%Y-%m-%d %H:%M")

    dateFrom = request.args.get('dateFrom')
    dateTo = request.args.get('dateTo')
    requestFile = request.args.get('request')
    dateFrom = datetime.strptime(dateFrom, '%Y-%m-%d') if dateFrom else monthAgo
    dateTo = datetime.strptime(dateTo, '%Y-%m-%d') if dateTo else fullDateTimeNow
    if dateTo < dateFrom: dateFrom, dateTo = dateTo, dateFrom

    if dep == 'host1':
        ldapGroup = 'ovpn1'
        users = DB1.query.order_by(DB1.id).all()
        ldapResult = ldapFunc.connectionLdap(ldapGroup)
        ldapUser = ldapFunc.getUser(ldapGroup, user)
        ldapCN = ldapUser[0][0].split(',')[0].split('=')[1]
        ldapLogin = ldapUser[0][1].get("sAMAccountName")[0].decode("utf-8").replace('$','')
        userDTs = DB1.query.with_entities(
                    DB1.since, DB1.datetime
                  ).filter(
                    DB1.login.contains(ldapLogin)
                  ).filter(
                    and_(DB1.datetime >= dateFrom, DB1.datetime <= dateTo + timedelta(days=1))
                  ).order_by(
                    DB1.id.desc()
                  ).all()
    elif dep == 'host2':
        ldapGroup = 'ovpn2'
        users = DB2.query.order_by(DB2.id).all()
        ldapResult = ldapFunc.connectionLdap(ldapGroup)
        ldapUser = ldapFunc.getUser(ldapGroup, user)
        ldapCN = ldapUser[0][0].split(',')[0].split('=')[1]
        ldapLogin = ldapUser[0][1].get("sAMAccountName")[0].decode("utf-8").replace('$','')
        userDTs = DB2.query.with_entities(
                    DB2.since, DB2.datetime
                  ).filter(
                    DB2.login.contains(ldapLogin)
                  ).filter(
                    and_(DB2.datetime >= dateFrom, DB2.datetime <= dateTo + timedelta(days=1))
                  ).order_by(
                    DB2.id.desc()
                  ).all()
    elif dep == 'host3':
        ldapGroup = 'ovpn3'
        users = DB3.query.order_by(DB3.id).all()
        ldapResult = ldapFunc.connectionLdapDB3()
        ldapUser = ldapFunc.getUserDB3(user)
        ldapCN = ldapUser[0][0].split(',')[0].split('=')[1]
        ldapLogin = ldapUser[0][1].get("sAMAccountName")[0].decode("utf-8").replace('$','')
        userDTs = DB3.query.with_entities(
                    DB3.since, DB3.datetime
                  ).filter(
                    DB3.login.contains(ldapLogin)
                  ).filter(
                    and_(DB3.datetime >= dateFrom, DB3.datetime <= dateTo + timedelta(days=1))
                  ).order_by(
                    DB3.id.desc()
                  ).all()
    else:
        return redirect('/')

    q = request.args.get('q')
    if q:
        ldapUser = ldapFunc.getUser(ldapGroup, q)
        if ldapUser: return redirect("/" + dep + "/" + ldapUser[0][0].split(',')[0].split('=')[1])

    lastDT = datetime(1970, 1, 1)
    correctUserDTs, listDT, todayDTs = [], [], []
    for userDT in userDTs:
        correctUserDTs.append([datetime.fromtimestamp(int(float(userDT[0]))), userDT[1]])
    for userDT in correctUserDTs:
        if userDT[1] > lastDT: lastDT = userDT[1]
    if lastDT.strftime("%Y-%m-%d %H:%M") >= datetimeNow:
        lastDT = "connected"
    elif lastDT == datetime(1970, 1, 1):
        lastDT = "нет данных"
    for corUserDT in correctUserDTs:
        if corUserDT[0] > corUserDT[1]: corUserDT[0], corUserDT[1] = corUserDT[1], corUserDT[0]
        listDT.append([corUserDT[0], corUserDT[1], corUserDT[1] - corUserDT[0]])
        if corUserDT[1].strftime("%Y-%m-%d") == fullDateTimeNow.strftime("%Y-%m-%d"):
            todayDTs.append([corUserDT[0], corUserDT[1], corUserDT[1] - corUserDT[0]])
    # List of: ldap CName, ldap sAMAccountName(login), db last user datetime, db today user datetime, db all user datetimes
    ldapADUser = [ldapCN, ldapLogin, lastDT, todayDTs, listDT]
    dateFrom = datetime.strptime(dateFrom.strftime("%Y-%m-%d"), '%Y-%m-%d')
    dateTo = datetime.strptime(dateTo.strftime("%Y-%m-%d"), '%Y-%m-%d')
    if requestFile == 'csv':
        csvBody = ldapCN + ",,\nНачало,Конец,Время\n"
        for string in listDT:
            csvBody = csvBody + str(string[0]) + ',' + str(string[1]) + ',' + str(string[2]) + '\n'
        return Response(csvBody, mimetype="text/csv", \
                        headers={"Content-disposition": "attachment; filename=" + ldapLogin + ".csv"})
    return render_template("user.html", user=ldapADUser, dateFrom=dateFrom, dateTo=dateTo, server=dep)


@app.route('/host4')
def dev():
    return render_template("dev.html")


if __name__ == "__main__":
    app.run(debug=False)
