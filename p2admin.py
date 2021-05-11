uinfo = {'mail': 'not logged in'}
cur = []
conn = []


def grant():
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    cur.execute(
        '''SELECT p6 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        print("You don't have permissions to use this function")
        return
    if not(auth[0]):
        print("You don't have permissions to use this function")
        return
    pass


def newCred():
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    pass


def getCreds():
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    pass


def killSub():
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    pass


def notArtist():
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    pass


def bitacora():
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    cur.execute(
        '''SELECT p8 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        print("You don't have permissions to use this function")
        return
    if not(auth[0]):
        print("You don't have permissions to use this function")
        return
    pass
