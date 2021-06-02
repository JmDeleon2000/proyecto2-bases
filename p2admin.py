import sqlite3 as sql
import random
from random import randint

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
        cur.execute('''SELECT * FROM users WHERE mail = %s''', (arg,))
        res = cur.fetchone()
        # mod_users(u_id int, sub boolean, reps int, sub_date date, per int, is_banned boolean, changer varchar)
        cur.execute('''SELECT * FROM mod_users(%s, %s, %s, %s, %s, %s, %s)''',
                    (res[0], False, res[5], res[6], res[7], res[8], uinfo['mail']))
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
            '''SELECT artistid FROM artist WHERE artistname = %s''', (arg,))
        res = cur.fetchone()[0]
        # mod_artist(artist_id int, artist_name varchar, n_activo boolean, changer varchar)
        cur.execute(
            '''SELECT * FROM mod_artist(%s, %s, %s, %s)''', (res, arg, False, uinfo['mail']))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def bitacora():  # tested
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
    try:
        print('users:')
        cur.execute('''SELECT * FROM users_log''')
        users = cur.fetchall()
        for i in users:
            print(i)
        print('Artists: ')
        cur.execute('''SELECT * FROM artist_log''')
        artist = cur.fetchall()
        for i in artist:
            print(i)
        print('songs: ')
        cur.execute('''SELECT * FROM song_log''')
        song = cur.fetchall()
        for i in song:
            print(i)
        print('playlists: ')
        cur.execute('''SELECT * FROM playlist_log''')
        pl = cur.fetchall()
        for i in pl:
            print(i)
        print('songs: ')
        cur.execute('''SELECT * FROM album_log''')
        album = cur.fetchall()
        for i in album:
            print(i)
        conn.commit()
    except:
        print('Something went wrong with the connection')
        conn.rollback()


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


def enable_song():  # ver permisos aca
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    cur.execute(
        '''SELECT p2 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        print("You don't have permissions to use this function")
        return
    if not(auth[0]):
        print("You don't have permissions to use this function")
        return
    arg = input(
        'Do you want the song to be enabled (visible)? (y for yes or n for no): ')
    if arg == 'y':
        vis = True
    elif arg == 'n':
        vis = False
    else:
        print('Error, make sure to use lower case y or n')
        return
    song = input(
        'Provide the name of the song you want to enable or disable: ')
    cur.execute('''SELECT * FROM song WHERE name = %s''', (song,))
    song = cur.fetchone()
    if song:
        try:
            # mod_song(song_id int, n_artist int, n_name varchar, n_genre varchar,
            #							n_album int, n_reps int, n_visible boolean, n_iframe varchar, changer varchar)
            cur.execute('''SELECT * FROM mod_song(%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                        (song[0], song[1], song[2], song[3], song[4], song[5], vis, song[7], uinfo['mail'],))
            conn.commit()
        except:
            conn.rollback()
            print('Something went wrong with the connection')
    else:
        print("That song doesn't exist")
        return


def enable_album():
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    cur.execute(
        '''SELECT p2 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        print("You don't have permissions to use this function")
        return
    if not(auth[0]):
        print("You don't have permissions to use this function")
        return
    arg = input(
        'Do you want the album to be enabled (visible)? (y for yes or n for no): ')
    if arg == 'y':
        vis = True
    elif arg == 'n':
        vis = False
    else:
        print('Error, make sure to use lower case y or n')
        return
    album = input(
        'Provide the name of the album you want to enable or disable: ')
    cur.execute('''SELECT albumid FROM album WHERE name = %s''', (album,))
    albumid = cur.fetchone()
    if not(albumid):
        print("That album doesn't exist")
        return
    cur.execute('''SELECT * FROM song WHERE album = %s''', (albumid[0],))
    songs = cur.fetchall()
    if songs:
        try:
            # mod_song(song_id int, n_artist int, n_name varchar, n_genre varchar,
            #							n_album int, n_reps int, n_visible boolean, n_iframe varchar, changer varchar)
            for song in songs:
                cur.execute('''SELECT * FROM mod_song(%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                            (song[0], song[1], song[2], song[3], song[4], song[5], vis, song[7], uinfo['mail'],))
            conn.commit()
        except:
            conn.rollback()
            print('Something went wrong with the connection')
    else:
        print("That song doesn't exist")
        return

songlist1 = [
    'hi',
    'tree',
    'sky',
    'mate',
    'water',
    'drops',
    'te',
    'tv',
    'happy',
    'cellphone',
    'miss',
    'you',
    'music',
    'crazy',
    'lens',
    'maybe',
    'whatever',
    'bye',
    'my',
    'mouse'
]

songlist2 = [
    'lover',
    'Ericka',
    'horse',
    'rave',
    'crazy',
    'haha',
    'sushi',
    'restaurant',
    'sky',
    'rain',
    'sad',
    'hehe',
    'balloon',
    'recipe',
    'facade',
    'mad',
    'pet',
    'lotion'
]

songlist3 = [
    'cat',
    'dog',
    'random',
    'belive',
    'ring',
    'plate',
    'enemy',
    'Lacoste',
    'Adidas',
    'Nike',
    'note',
    'forget',
    'floor',
    'book',
    'picture',
    'you',
    'lie',
    'fall',
    'Kodak'
]

genrelist = [
    'Rock',
    'Pop',
    'Rap',
    'Hip hop',
    'Dubstep',
    'Balade',
    'Alternative',
    'Reggaeton',
    'Sab hop',
    'Metal',
    'Ambient',
    'EDM',
    'R&B',
    'Bedroomrock',
    'Synthpop',
    'Soul',
    'Neofolk'
]

songnames = []

def generate_random_song():
    fir = random.choice(songlist1)
    sec = random.choice(songlist2)
    thir = random.choice(songlist3)
    song = f'{fir} {sec} {thir}'
    return song

#random.sample(range(40, 99999), tracks)

def insert_song(reps, songid, artist, name, genre, album):
    '''songid = random.sample(range(40, 9999), tracks)
    artist = random.sample(range(1, 24), tracks)
    name = generate_random_song()
    genre = random.choice(genrelist)
    album = random.sample(range(1, 23), tracks)
    reps = random.sample(range(reps), tracks)'''
    query = f'''INSERT INTO song(songid, artist, name, genre, album, reps, visible, iframe) VALUES('''+str(songid)+''', '''+str(artist)+''', '''+ "'" + str(name) + "'" + ''', ''' + "'" + str(genre) + "'" + ''','''+str(album)+''',''' +str(reps)+''', TRUE, NULL)'''
    cur.execute(query)
    return query

def insert_sale(song, date):
    
    query = f'''INSERT INTO sales VALUES ('''+ "'" + str(song) + "'" + ''', '''+ "'" + str(date) + "'" + ''', 1)'''
    cur.execute(query)
    return query

def simulation():
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    cur.execute(
        '''SELECT p7 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        print("You don't have permissions to use this function")
        return
    if not(auth[0]):
        print("You don't have permissions to use this function")
        return
    date = input('\n Enter date to simulate YYYY-MM-DD\n')
    tracks = input('\n Enter number of tracks to simulate\n')
    reps = input('\n Enter max number of reps to simulate\n')
    rep = int(reps)
    track = int(tracks)
    songid = random.sample(range(40, 9999), track)
    artist = random.sample(range(1, 24), track)
    genre = random.choice(genrelist)
    album = random.sample(range(1, 23), track)
    repe = random.sample(range(rep), track)

    for i in range(0, track):
        name = generate_random_song()
        songidnotrep = random.choice(songid)
        songid.remove(songidnotrep)
        insert_song(random.choice(repe), songidnotrep, random.choice(artist), name, genre, random.choice(album))

    for i in range(0, rep):
        insert_sale(randint(1,32), date)
    
    
    print("Simulation finished")
    conn.commit()
        