import psycopg2
from psycopg2 import Error
import user
import reports
import p2admin

connection = psycopg2.connect(user = "postgres",
                                      password = "123456",
                                      host = "localhost",
                                      port = "5433",
                                      database = "proyecto2")
cur = connection.cursor()
user.cur = cur
user.conn = connection
p2admin.cur = cur
p2admin.conn = connection


def help():
    for i in cli.keys():
        print(i + ': ' + cli[i]['descript'])
        
def login():
    mail = input('please enter you e-mail: ')
    pw = input('please enter your password: ')
    try:
        cur.execute(
            '''select pw, admin, uid, suscrito, plays, credenciales from users where mail = %s and banned = false''', (mail,))
        res = cur.fetchone()
        if not(res):
            print('Wrong e-mail or password')
            return
        if res[0] == pw:
            uinfo['mail'] = mail
            uinfo['admin'] = res[1]
            uinfo['sub'] = res[3]
            uinfo['plays'] = res[4]
            uinfo['uid'] = res[2]
            uinfo['cred'] = res[5]
            uinfo['playstoday'] = 0
            cur.execute(
                'select artistname from users inner join artist on  artist.artistid = {id}'.format(id=res[2]))
            if cur.fetchone():
                uinfo['artist'] = True
            else:
                uinfo['artist'] = False
            print('Login succesful')
        else:
            print('Wrong e-mail or password')
        connection.commit()
        print(uinfo)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Email no registrado", error)
    user.uinfo = uinfo
    p2admin.uinfo = uinfo


cli = {
    "help": {"descript": "shows how to invoke all commands and their own description\nPlease enter the name of the commands to use them", "func": help},
    'login': {"descript": "logs in as a given user", "func": login},
    'register': {"descript": "creates a new account", "func": user.register},
    'play': {"descript": "plays a given song", "func": user.play},
    'byAlbum': {"descript": "searches songs by album name", "func": user.byAlbum},
    'byArtist': {"descript": "searches songs by artist name", "func": user.byArtist},
    'byGenre': {"descript": "searches songs by artist name", "func": user.byGenre},
    'subscribe': {"descript": "adds a subscription allowing for indefinite playtime and creating playlists", "func": user.subscribe},
    'playlist': {"descript": "plays a given playlist", "func": user.playlist},
    'addto': {"descript": "adds a song to a playlist", "func": user.addto},
    # 'next':{"descript":"plays the next song in the current playlist", "func":user.next},
    # 'last':{"descript":"plays the last song in the current playlist", "func":user.last},
    'CreatePlaylist': {"descript": "creates a playlist", "func": user.newpl},
    'getPlaylists': {"descript": "shows all playlists owned by you", "func": user.getpls},
    'reports': {"descript": "shows reports on a period of time", "func": user.reports},
    'records': {"descript": "shows part 2 of reports on a period of time", "func": user.ventanaRecords},
    'earnings': {"descript": "report of how much earning a song has", "func": user.earnings},
    'createCredentialProfile': {"descript": "Creates a new credentials profile", "func": p2admin.newCred},
    'grantPermissions': {"descript": "Grants a credential profile to a user", "func": p2admin.grant},
    'getCredentialProfiles': {"descript": "Shows all previously created credential profiles", "func": p2admin.getCreds},
    'deactivateArtists': {"descript": "Blocks an artist from using artist features", "func": p2admin.DeactivateArtist},
    'showLogs': {"descript": "Shows all log changes", "func": p2admin.bitacora},
    'removeSubscription': {"descript": "Cancels a subscription", "func": p2admin.killSub},
    'ban': {"descript": "Bans an unsubscribed user", "func": p2admin.ban},


}

uinfo = {'mail':'not logged in'}

end = False
while not(end):
    res = input('Proyecto2: ' + str(uinfo['mail']) + '-> ')
    if res in cli.keys():
        cli[res]['func']()
    else:
        print('Not a valid command. Use the command help to see all avalible commands')
