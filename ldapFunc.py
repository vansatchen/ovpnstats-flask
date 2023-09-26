import ldap

ldapServer1 = "example1.com"
ldapServer2 = "example2.com"
ldapUser = "ldapUser@example.com"
ldapPass = "ldapPass"
base = "OU=path,DC=example,DC=com"
scope = ldap.SCOPE_SUBTREE
attrs = ['sAMAccountName','mail']

def testConnect(server):
    global lconn
    try:
        lconn = ldap.initialize('ldap://%s:389' % server)
        lconn.protocol_version = ldap.VERSION3
        lconn.set_option(ldap.OPT_REFERRALS, 0)
        lconn.simple_bind_s(ldapUser, ldapPass)
        return True
    except ldap.SERVER_DOWN:
        print("Error connection to %s" % server)
        return False

def connectionLdap(group):
    filter = "(memberOf=CN=" + group + ",OU=vpn,OU=Groups,DC=example,DC=com)"
    status = testConnect(ldapServer1)
    if not status:
        status = testConnect(ldapServer2)
        if not status: exit()

    # Search for members in group
    ldap_result_id = lconn.search_s(base, scope, filter, attrs)
    return sorted(ldap_result_id)

def getUser(group, CN):
    status = testConnect(ldapServer1)
    if not status:
        status = testConnect(ldapServer2)
        if not status: exit()

    # Search for member in group
    filter = "(&(cn=" + CN + "*)(memberOf=CN=" + group + ",OU=vpn,OU=Groups,DC=example,DC=com))"
    ldap_result_id = lconn.search_s(base, scope, filter, attrs)

    return ldap_result_id

def getUserDB3(CN):
    status = testConnect(ldapServer1)
    if not status:
        status = testConnect(ldapServer2)
        if not status: exit()

    # Search for member in group
    filter = "(&(cn=" + CN + "*)(memberOf=CN=path,OU=vpn,OU=Groups,DC=example,DC=com))"
    base = "OU=pc,OU=path,OU=vpn,OU=Groups,DC=example,DC=com"
    ldap_result_id = lconn.search_s(base, scope, filter, attrs)

    return ldap_result_id

def connectionLdapDB3():
    filter = "(memberOf=CN=path,OU=vpn,OU=Groups,DC=example,DC=com)"
    base = "OU=pc,OU=path,OU=vpn,OU=Groups,DC=example,DC=com"
    status = testConnect(ldapServer1)
    if not status:
        status = testConnect(ldapServer2)
        if not status: exit()

    # Search for members in group
    ldap_result_id = lconn.search_s(base, scope, filter, attrs)
    return sorted(ldap_result_id)
