uinfo = {'mail':'not logged in'}
cur = []
conn = []

def play():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
        return
    print(uinfo)
def byAlbum():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
        return
    arg = input('Please enter the name of the album you want to search for: ')
    
    try:
        cur.execute('''SELECT song.name FROM song INNER JOIN album ON song.album = album.albumid WHERE album.name = %s''', (arg,))
        res = cur.fetchall()
        conn.commit()
        if not(res):
            print('No songs found for that album')
        for i in res:
            print(i[0])
    except:
        print("Error, something went wrong with the connection")
        
def byGenre():
    if uinfo == {'mail':'not logged in'}:
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
        print("Error, something went wrong with the connection")
def byArtist():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
        return
    arg = input('Please enter the name of the artist you want to search for: ')
    
    try:
        cur.execute('''SELECT song.name FROM song INNER JOIN album ON song.artist = artistid WHERE artist.artistname = %s''', (arg,))
        res = cur.fetchall()
        conn.commit()
        if not(res):
            print('No songs found for that artist')
        for i in res:
            print(i[0])
    except:
        print("Error, something went wrong with the connection")
        
def subscribe():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
        return
    if uinfo['sub']:
        print('You are already subscribed')
        return
    try:
        cur.execute('UPDATE users SET suscrito = True  WHERE uid = {user}'.format(user = uinfo['uid']))
        conn.commit()
        uinfo['sub'] = True
    except:
        print("Error, couldn't subscribe")
    
def playlist():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
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
        print('Something went wrong with the connection')
    pass
def addto():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
        return
    pass
def next():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
        return
    pass
def last():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
        return
    pass
def newpl():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
        return
    pass
def getpls():
    if uinfo == {'mail':'not logged in'}:
        print('You need to login first')
        return
    pass
def register():
    pass