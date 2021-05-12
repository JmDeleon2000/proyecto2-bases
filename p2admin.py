uinfo = {'mail': 'not logged in'}
cur = []
conn = []


def grant():  # todo
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
    arg = input(
        'Provide the e-mail of the user you want to grant permissions to: ')
    cur.execute('''SELECT * FROM users WHERE mail = %s''', (arg,))
    user = cur.fetchone()
    if not(user):
        print('The user was not found')
        return
    arg = input(
        'Provide the name of the credential profile you want to grant to the user: ')
    cur.execute('''SELECT * FROM cred WHERE name = %s''', (arg,))
    cred = cur.fetchone()
    if not(cred):
        print('The credential profile was not found')
        return
    try:
        # mod_users(u_id int, sub boolean, reps int, sub_date date, per int, is_banned boolean, changer varchar)
        cur.execute('''SELECT * FROM mod_users(%s, %s, %s, %s, %s, %s, %s)''',
                    (user[0], user[3], user[5], user[6], cred[0],  user[8], uinfo['mail']))
        conn.commit()
        print('The user has been granted the permissions')
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def newCred():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    if not(uinfo['admin']):
        print('You need to be an administrator to create credential profiles')
        return
    cred_name = input('Provide a name for the credential: ')
    cur.execute('''SELECT name FROM cred WHERE name = %s''', (cred_name,))
    if cur.fetchone():
        print('Please, use a name that has not been used before')
        return
    creds = {'p1': {'desc': "Profile can modify the information of any album or song?: ", 'val': False},
             'p2': {'desc': "Prfile can disable any albums or songs?: ", 'val': False},
             'p3': {'desc': "Block unsubscribed users?: ", 'val': False},
             'p4': {'desc': "Cancel user subscriptions?: ", 'val': False},
             'p5': {'desc': "Deactivate users registered as artists?: ", 'val': False},
             'p6': {'desc': "Grant this kind of permissions (access to this function)?: ", 'val': False},
             'p7': {'desc': "Can get reports from the platform?: ", 'val': False},
             'p8': {'desc': "Can see the change logs?: ", 'val': False}, }
    for i in creds.keys():
        print('Awnser y for yes or n for no: ')
        print('The profile can')
        arg = input(creds[i]['desc'])
        if arg == 'y':
            creds[i]['val'] = True
    try:
        cur.execute(
            '''INSERT INTO cred (p1, p2, p3, p4, p5, p6, p7, p8, name) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (creds['p1']['val'], creds['p2']['val'], creds['p3']['val'], creds['p4']['val'],
             creds['p5']['val'], creds['p6']['val'], creds['p7']['val'], creds['p8']['val'], cred_name))
        print('The profile has been created')
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


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
        conn.commit()
    except:
        conn.rollback()
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


def ban():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    cur.execute(
        '''SELECT p3 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        print("You don't have permissions to use this function")
        return
    if not(auth[0]):
        print("You don't have permissions to use this function")
        return
    arg = input('Provide the e-mail of the user you want to ban: ')
    cur.execute('''SELECT * FROM users WHERE mail = %s''', (arg,))
    res = cur.fetchone()
    if not(res):
        print('The user was not found')
        return
    if res[3]:
        print('The user is subscribed so it cannot be banned')
        return
    try:
        # mod_users(u_id int, sub boolean, reps int, sub_date date, per int, is_banned boolean, changer varchar)
        cur.execute('''SELECT * FROM mod_users(%s, %s, %s, %s, %s, %s, %s)''',
                    (res[0], res[3], res[5], res[6], res[7], True, uinfo['mail']))
        conn.commit()
        print('The user has been banned')
    except:
        conn.rollback()
        print('Something went wrong with the connection')
