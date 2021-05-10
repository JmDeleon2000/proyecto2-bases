from datetime import datetime

uinfo = {'mail': 'not logged in'}
cur = []
conn = []


def play():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    arg = input("What's the name of the song you want to play?: ")
    if uinfo['playstoday'] >= 3 and not(uinfo['sub']):
        print('You need to subscribe to be able to play more than 3 songs a day')
        return
    uinfo['playstoday'] += 1
    try:
        cur.execute('''SELECT song.iframe FROM song WHERE name = %s''', (arg,))
        res = cur.fetchall()
        if not(res):
            print("We couldn't find that song. Check if you wrote the name correctly")
            return
        cur.execute('''SELECT plays FROM users WHERE uid = %s''',
                    (uinfo['uid'],))
        PLAYS = cur.fetchone()[0] + 1
        cur.execute('''UPDATE users SET plays = %s WHERE uid = %s''',
                    (PLAYS, uinfo['uid']))
        conn.commit()
        for i in res:
            print(i[0])
    except:
        conn.rollback()
        print("Error, something went wrong with the connection")


def byAlbum():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    arg = input('Please enter the name of the album you want to search for: ')
    try:
        cur.execute(
            '''SELECT song.name FROM song INNER JOIN album ON song.album = album.albumid WHERE album.name = %s''', (arg,))
        res = cur.fetchall()
        conn.commit()
        if not(res):
            print('No songs found for that album')
        for i in res:
            print(i[0])
    except:
        conn.rollback()
        print("Error, something went wrong with the connection")


def byGenre():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    arg = input('Please enter the name of the genre you want to search for: ')

    try:
        cur.execute('''SELECT song.name FROM song WHERE genre = %s''', (arg,))
        res = cur.fetchall()
        conn.commit()
        if not(res):
            print('No songs found for that for that genre')
        for i in res:
            print(i[0])
    except:
        conn.rollback()
        print("Error, something went wrong with the connection")


def byArtist():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    arg = input('Please enter the name of the artist you want to search for: ')

    try:
        cur.execute(
            '''SELECT song.name FROM song INNER JOIN artist ON song.artist = artistid WHERE artist.artistname = %s''', (arg,))
        res = cur.fetchall()
        conn.commit()
        if not(res):
            print('No songs found for that artist')
        for i in res:
            print(i[0])
    except:
        conn.rollback()
        print("Error, something went wrong with the connection")


def subscribe():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    if uinfo['sub']:
        print('You are already subscribed')
        return
    try:
        cur.execute('''UPDATE users SET suscrito = True  WHERE uid = %s''',
                    (uinfo['uid'], datetime.now(),))
        conn.commit()
        uinfo['sub'] = True
    except:
        conn.rollback()
        print("Error, couldn't subscribe")


def playlist():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    if not(uinfo['sub']):
        print('You need to be a subscriber to use playlists')
        return
    arg = input('Enter the name of the playlist you want to play: ')
    try:
        cur.execute('''SELECT song.name, iframe
FROM plentry ple INNER JOIN playlist pl ON ple.playlist = pl.plid
INNER JOIN song ON ple.song = songid WHERE pl.name = %s AND pl.users = %s''', (arg, uinfo['uid']))

        res = cur.fetchall()
        conn.commit()
        if not(res):
            print("The playlist is empty or doesn't exist")
        for i in res:
            print(i[0])
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def addto():
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    if not(uinfo['sub']):
        print('You need to be a subscriber to use playlists')
        return
    plname = input(
        "Please provide the name of the playlist you want to add a song to: ")
    cur.execute(
        '''SELECT name, plid FROM playlist WHERE  name = %s''', (plname,))
    plinfo = cur.fetchone()
    if plinfo:
        songname = input(
            "Please input the name of the song you want to add to " + plname + ": ")
        cur.execute(
            '''SELECT name, songid FROM song WHERE  name = %s''', (songname,))
        songinfo = cur.fetchone()
        if not(songinfo):
            conn.rollback()
            print("That song doesn't exist")
            return
        cur.execute(
            '''SELECT entryid+1 FROM plentry WHERE playlist = %s ORDER BY entryid DESC LIMIT 1''', (plinfo[1],))
        entryid = cur.fetchone()
        if not(entryid):
            entryid = (0,)
        cur.execute('''INSERT INTO plentry VALUES(%s, %s, %s)''',
                    (entryid[0], plinfo[1], songinfo[1]))
        conn.commit()
    else:
        conn.rollback()
        print('Please check for the playlist existing or the name being misspelled')


def newpl():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    if not(uinfo['sub']):
        print('You need to be a subscriber to use playlists')
        return
    arg = input('Provide a name for the new playlist: ')
    try:
        cur.execute('''SELECT name FROM playlist WHERE name = %s''', (arg,))
        if not(cur.fetchone()):
            cur.execute(
                '''SELECT plid FROM playlist ORDER BY plid DESC LIMIT 1''', (arg,))
            ID = cur.fetchone()[0]+1
            cur.execute('''INSERT INTO playlist VALUES(%s, %s, %s)''',
                        (ID, arg, uinfo['uid'],))
            conn.commit()
        else:
            conn.rollback()
            print("Please, use a name you haven't used for other playlist")
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def getpls():  # tested
    if uinfo == {'mail': 'not logged in'}:
        print('You need to login first')
        return
    if not(uinfo['sub']):
        print('You need to be a subscriber to use playlists')
        return
    try:
        cur.execute(
            '''SELECT name FROM  playlist WHERE users = %s''', (uinfo['uid'],))
        res = cur.fetchall()
        conn.commit()
        if not(res):
            print("Haven't created any playlists")
        for i in res:
            print(i[0])
    except:
        conn.rollback()
        print('Something went wrong with the connection')


def register():
    uname = input("Please provide an e-mail: ")
    password = input("Please provide a password: ")
    try:
        cur.execute('''SELECT mail FROM users WHERE mail = %s''', (uname,))
        if cur.fetchone():
            print('That e-mail is already in use')
            return
        cur.execute('''SELECT uid FROM users ORDER BY uid DESC LIMIT 1''')
        ID = cur.fetchone()[0]+1
        cur.execute('''INSERT INTO users(uid, mail, pw, suscrito, admin, plays)
VALUES(%s, %s, %s, false, false, 0)''', (ID, uname, password))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')
