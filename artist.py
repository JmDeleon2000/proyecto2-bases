from datetime import datetime

uinfo = {'mail': 'not logged in'}
cur = []
conn = []


def new_artist():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    # new_artist(artist_id int, artist_name varchar, changer varchar)
    arg = input('Provide your artist name: ')
    try:
        cur.execute('''SELECT * FROM new_artist(%s, %s, %s)''',
                    (uinfo['uid'], arg, uinfo['mail'],))
        uinfo['artist'] = True
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def change_name():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    if not(uinfo['artist']):
        print('You are not permited to use artist functions')
        return
    # mod_artist(artist_id int, artist_name varchar, n_activo boolean, changer varchar)
    arg = input('Provide your new artist name: ')
    try:
        cur.execute('''SELECT * FROM mod_artist(%s, %s, %s, %s)''',
                    (uinfo['uid'], arg, True, uinfo['mail'],))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def new_song():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    if not(uinfo['artist']):
        print('You are not permited to use artist functions')
        return
    # new_song(song_id int, n_artist int, n_name varchar, n_genre varchar,
    # n_album int, n_reps int, visible boolean, n_iframe varchar, changer varchar)
    cur.execute('''SELECT songid+1 FROM song ORDER BY songid DESC LIMIT 1''')
    ID = cur.fetchone()[0]
    name = input("Provide the name of the song: ")
    genre = input("Provide the name of the genre: ")
    album = input("Provide the name of the album (leave blank if none): ")
    cur.execute('''SELECT albumid FROM album WHERE name = %s''', (album,))
    album = cur.fetchone()
    iframe = input("Provide the youtube link to the song: ")
    try:
        cur.execute('''SELECT * FROM new_song(%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (ID, uinfo['uid'], name, genre, album, 0, True, iframe, uinfo['mail'],))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def mod_song():  # verpermisos aca
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    per = True
    cur.execute(
        '''SELECT p1 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        if not(auth[0]):
            per = False
    if not(uinfo['artist'] or per):
        print('You are not permited to use this function')
        return
    # mod_song(song_id int, n_artist int, n_name varchar, n_genre varchar,
    # n_album int, n_reps int, n_visible boolean, n_iframe varchar, changer varchar)
    try:
        song = input('Enter the name of the song you want to change: ')
        cur.execute('''SELECT * FROM song WHERE name = %s''', (song,))
        song = cur.fetchone()
        if not(song):
            print('Song was not found')
            return
        name = input("Provide the name of the song: ")
        genre = input("Provide the name of the genre: ")
        album = input("Provide the name of the album (leave blank if none): ")
        cur.execute('''SELECT albumid FROM album WHERE name = %s''', (album,))
        album = cur.fetchone()
        iframe = input("Provide the youtube link to the song: ")
        cur.execute('''SELECT * FROM new_song(%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (song[0], song[1], name, genre, album, song[5], song[6], iframe, uinfo['mail'],))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def new_album():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    # new_album(album_id integer, artist_id integer, n_name character varying, changer character varying)
    if not(uinfo['artist']):
        print('You are not permited to use artist functions')
        return
    try:
        cur.execute(
            '''SELECT albumid + 1 FROM album ORDER BY albumid DESC LIMIT 1''')
        ID = cur.fetchone()[0]
        name = input('Provide the name of the album: ')
        cur.execute('''SELECT * FROM new_album(%s, %s, %s, %s)''',
                    (ID, uinfo['uid'], name, uinfo['mail'],))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def mod_album():  # verpermisos aca
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    per = True
    cur.execute(
        '''SELECT p1 FROM users INNER JOIN cred ON users.credenciales = credid WHERE uid = %s''', (uinfo['uid'], ))
    auth = cur.fetchone()
    if not(auth):
        if not(auth[0]):
            per = False
    if not(uinfo['artist'] or per):
        print('You are not permited to use this function')
        return
    try:
        # mod_album(album_id integer, artist_id integer, n_name character varying, n_release date, changer character varying)
        name = input('Provide the name of the album: ')
        cur.execute(
            '''SELECT * FROM album WHERE name = %s''', (name,))
        album = cur.fetchone()
        n_name = input('Provide the new name of the album: ')
        n_date = datetime.strptime(
            input('Write the new release date (12-25-2000): '), '%m-%d-%Y')
        cur.execute('''SELECT * FROM mod_album(%s, %s, %s, %s::date, %s)''',
                    (album[0], album[1], n_name, n_date, uinfo['mail'],))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')
