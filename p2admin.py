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
    if not(uinfo['admin']):
        print('You need to be an administrator to create credential profiles')
        return
    pass


def getCreds():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    try:
        cur.execute('''SELECT * FROM cred''')
        res = cur.fetchall()
        for i in res:
            print('Name: ' + str(i[9]) + ': ')
            print('     Modifiy tracks: ' + str(i[1]))  # todo
            print('     Deactivate tracks: ' + str(i[2]))  # todo
            print('     Block users: ' + str(i[3]))  # todo
            print('     Unsubscribe users: ' + str(i[4]))
            print('     Deactivate artists: ' + str(i[5]))
            print('     Grant permissions: ' + str(i[6]))  # todo
            print('     Get reports: ' + str(i[7]))  # todo
            print('     Check logs: ' + str(i[8]))  # todo
    except:
        print('Something went wrong with the connection')
    pass


def killSub():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    cur.execute(
        '''SELECT p4 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        print("You don't have permissions to use this function")
        return
    if not(auth[0]):
        print("You don't have permissions to use this function")
        return
    arg = input(
        'Provide the e-mail of the user whose subscription you want to cancel: ')
    try:
        cur.execute(
            '''UPDATE users SET suscrito = false WHERE mail = %s''', (arg,))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def DeactivateArtist():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    cur.execute(
        '''SELECT p5 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        print("You don't have permissions to use this function")
        return
    if not(auth[0]):
        print("You don't have permissions to use this function")
        return
    arg = input('Provide the name of the artist you want to deactivate: ')
    try:
        cur.execute(
            '''UPDATE artist SET activo = false WHERE artistname = %s''', (arg,))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


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
