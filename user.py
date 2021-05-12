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
        cur.execute('''select * from new_users(%s, %s, %s, %s)''',
                    (ID, uname, password, uname))
        conn.commit()
    except:
        conn.rollback()
        print('Something went wrong with the connection')

import tkinter as tk
from tkinter import messagebox
from random import randint
from tkinter import Entry
from tkinter import ttk
import psycopg2
from psycopg2 import Error
from tkcalendar import *

uinfo = {'mail': 'not logged in'}
cur = []
conn = []


def reports():
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
    arg = input('\n Reports: \n 1. Most recent albums \n 2. Most popular artist \n 3. New users \n 4. Artist with more tracks \n 5. Most popular genres \n 6. Most active users \n')
    arg = int(arg)
    if arg == 1:
        try:
            cur.execute(
                '''SELECT name, release_date FROM album  WHERE release_date > '2021-03-20' ORDER BY release_date DESC limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
            for row in res:
                print("Name =", row[0])
                print("Release date =", row[1])
                print("\n")
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")

    elif arg == 2:
        try:
            cur.execute(
                '''SELECT artistname as name FROM artist  INNER JOIN song ON song.artist = artistid GROUP BY artistname ORDER BY sum(song.reps) LIMIT 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
            for row in res:
                print("Artist name =", row[0])
                print("\n")
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")

    elif arg == 3:
        try:
            cur.execute(
                '''SELECT count(subdate) as name FROM users WHERE subdate > '2020-09-01' limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
            for row in res:
                print("New users the past 3 months =", row[0])
                print("\n")
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")

    elif arg == 4:
        try:
            cur.execute('''SELECT artist.artistname as name, count(artist.artistname) FROM song INNER JOIN artist ON song.artist = artist.artistid GROUP BY artistname ORDER BY count DESC limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
            for row in res:
                print("Artist name =", row[0])
                print("Number of tracks =", row[1])
                print("\n")
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")

    elif arg == 5:
        try:
            cur.execute(
                '''SELECT  genre as name FROM song GROUP BY genre order BY count(*) DESC limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
            for row in res:
                print("Genre =", row[0])
                print("\n")
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")

    elif arg == 6:
        try:
            cur.execute(
                '''SELECT mail as name, plays FROM users order BY plays DESC limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
            for row in res:
                print("User =", row[0])
                print("Songs played =", row[1])
                print("\n")
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")

    else:
        print('bruh')

############################
######  REPORTERIA 2   #####
############################


def ventasSemanales(inicio, final):
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
    try:

        connection = psycopg2.connect(user = "postgres",
                                      password = "123456",
                                      host = "localhost",
                                      port = "5433",
                                      database = "proyecto2")
        cursor = connection.cursor()

        create_table_query = '''SELECT count(name) as sales, name
FROM sales INNER JOIN song ON sales.song = song.songid
WHERE sales.saledate > '''+ "'" + inicio + "'" + ''' and sales.saledate < ''' + "'" + final + "'" + '''
GROUP BY name
ORDER BY sales DESC'''

        cursor.execute(create_table_query)

        result = cursor.fetchall()

        connection.commit()

        for row in result:
            print("Sales =", row[0])
            print("Song name =", row[1])
            print("\n")

        #messagebox.showinfo(message=result, title="Consulta")
    except (Exception, psycopg2.DatabaseError) as error:
        messagebox.showerror(
            message="No se encontro el producto.", title="Consulta fallida")
        print("No se pudo realizar lo solicitado", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def ventasArtista(inicio, final, cantidad):
    try:

        connection = psycopg2.connect(user = "postgres",
                                      password = "123456",
                                      host = "localhost",
                                      port = "5433",
                                      database = "proyecto2")
        cursor = connection.cursor()

        create_table_query = '''SELECT count(name) as sales, name, artist.artistname
FROM sales INNER JOIN song ON sales.song = song.songid INNER JOIN artist ON song.artist = artist.artistid
WHERE sales.saledate > '''+ "'" + inicio + "'" + ''' and sales.saledate < ''' + "'" + final + "'" + '''
GROUP BY name, artist.artistname
ORDER BY sales DESC LIMIT ''' + cantidad

        cursor.execute(create_table_query)

        result = cursor.fetchall()

        for row in result:
            print("Sales =", row[0])
            print("Song  =", row[1])
            print("Artist =", row[2])
            print("\n")

        connection.commit()

        #messagebox.showinfo(message=result, title="Consulta")
    except (Exception, psycopg2.DatabaseError) as error:
        messagebox.showerror(
            message="No se encontro el producto.", title="Consulta fallida")
        print("No se pudo realizar lo solicitado", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def ventasGenero(inicio, final, cantidad):
    try:

        connection = psycopg2.connect(user = "postgres",
                                      password = "123456",
                                      host = "localhost",
                                      port = "5433",
                                      database = "proyecto2")
        cursor = connection.cursor()

        create_table_query = '''SELECT count(name) as sales, song.genre
FROM sales INNER JOIN song ON sales.song = song.songid 
WHERE sales.saledate > '''+ "'" + inicio + "'" + ''' and sales.saledate < ''' + "'" + final + "'" + '''
GROUP BY song.genre
ORDER BY sales DESC LIMIT ''' + cantidad

        cursor.execute(create_table_query)

        result = cursor.fetchall()

        for row in result:
            print("Sales =", row[0])
            print("Genre =", row[1])
            print("\n")

        connection.commit()

        #messagebox.showinfo(message=result, title="Consulta")
    except (Exception, psycopg2.DatabaseError) as error:
        messagebox.showerror(
            message="No se encontro el producto.", title="Consulta fallida")
        print("No se pudo realizar lo solicitado", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def masRep(cantidad, artista):
    try:

        connection = psycopg2.connect(user = "postgres",
                                      password = "123456",
                                      host = "localhost",
                                      port = "5433",
                                      database = "proyecto2")
        cursor = connection.cursor()

        create_table_query = '''SELECT artist.artistname, name, reps
FROM song INNER JOIN artist ON song.artist = artist.artistid
WHERE artist.artistname = '''+ "'" + artista + "'" + '''
GROUP BY artist.artistname, name, reps
ORDER BY reps DESC LIMIT ''' + cantidad

        cursor.execute(create_table_query)

        result = cursor.fetchall()

        for row in result:
            print("Artist =", row[0])
            print("Song name =", row[1])
            print("Reps =", row[2])
            print("\n")

        connection.commit()

        #messagebox.showinfo(message=result, title="Consulta")
    except (Exception, psycopg2.DatabaseError) as error:
        messagebox.showerror(
            message="No se encontro el producto.", title="Consulta fallida")
        print("No se pudo realizar lo solicitado", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


#######################
### Ventana grafica ###
#######################


def ventanaRecords():

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

    values = ["Total sales", "Top sales in artists",
              "Top sales by musical genre", "Most listened tracks by an artist"]

    def q1():
        date.configure(state="readonly")
        date2. configure(state="readonly")
        usuario.configure(state="disabled")
        combobox2.configure(state="disabled")

    def q2():
        date.configure(state="readonly")
        date2. configure(state="readonly")
        usuario.configure(state="disabled")
        combobox2.configure(state="readonly")

    def q3():
        date.configure(state="readonly")
        date2. configure(state="readonly")
        usuario.configure(state="disabled")
        combobox2.configure(state="readonly")

    def q4():
        date.configure(state="disabled")
        date2. configure(state="disabled")
        usuario.configure(state="normal")
        combobox2.configure(state="readonly")

    def method_unknown():
        label1.configure(text="unknown selected")

    def handler(event):
        current = combobox.current()
        value = values[current]
        print("current:", current, "value:", value)
        func_map = {
            "Total sales": q1,
            "Top sales in artists": q2,
            "Top sales by musical genre": q3,
            "Most listened tracks by an artist": q4

        }
        func = func_map.get(value, method_unknown)
        func()

    records = tk.Tk()
    records.title("Records")
    records.geometry("800x600")
    records.configure(background="LightGreen")

    label1 = tk.Label(records, text="Records", font=(
        "Century", 44), pady=40, bg="LightGreen", fg="black")
    label1.pack()

    campo1 = tk.Frame(records, bg="LightGreen")

    label1 = tk.Label(campo1, text="Record:", font=(
        "Courier", 20), bg="LightGreen", fg="black")
    label1.pack(side=tk.TOP)

    combobox = ttk.Combobox(campo1, width=50, values=[
                            "Total sales", "Top sales in artists", "Top sales by musical genre", "Most listened tracks by an artist"], state='readonly')
    combobox.bind("<<ComboboxSelected>>", handler)
    combobox.pack(side=tk.BOTTOM)
    combobox.current(0)

    campo1.pack(side=tk.TOP)

    label4 = tk.Label(records, text="", font=(
        "Courier", 17), bg="LightGreen", fg="black")
    label4.pack(side=tk.TOP)

    campo2 = tk.Frame(records, bg="LightGreen")
    label2 = tk.Label(campo2, text="Date:", font=(
        "Courier", 17), bg="LightGreen", fg="black")
    label2.pack(side=tk.TOP)

    label2 = tk.Label(campo2, text="Initiation:", font=(
        "Courier", 13), bg="LightGreen", fg="black")
    label2.pack(side=tk.LEFT, ipady=7)

    date = DateEntry(campo2, background='darkblue',
                     foreground='white', year=2021, state='readonly')
    date.pack(side=tk.LEFT)

    label3 = tk.Label(campo2, text="     End:", font=(
        "Courier", 13), bg="LightGreen", fg="black")
    label3.pack(side=tk.LEFT, ipady=7)

    date2 = DateEntry(campo2, background='darkblue',
                      foreground='white', year=2021, state='readonly')
    date2.pack(side=tk.LEFT)

    campo2.pack(side=tk.TOP)

    label4 = tk.Label(records, text="", font=(
        "Courier", 17), bg="LightGreen", fg="black")
    label4.pack(side=tk.TOP)

    campo3 = tk.Frame(records, bg="LightGreen")

    label4 = tk.Label(campo3, text="Complete information:",
                      font=("Courier", 17), bg="LightGreen", fg="black")
    label4.pack(side=tk.TOP)

    label5 = tk.Label(campo3, text="Artist:", font=(
        "Courier", 13), bg="LightGreen", fg="black")
    label5.pack(side=tk.LEFT, ipady=7)

    usuario = tk.Text(campo3, width=12, height=1, state="disabled")
    usuario.pack(side=tk.LEFT)

    label6 = tk.Label(campo3, text="   Amount:", font=(
        "Courier", 13), bg="LightGreen", fg="black")
    label6.pack(side=tk.LEFT, ipady=7)

    combobox2 = ttk.Combobox(campo3, width=10, values=[
                             10, 7, 5, 1], state='disabled')
    combobox2.pack(side=tk.LEFT)
    combobox2.current(0)

    campo3.pack(side=tk.TOP)

    label5 = tk.Label(records, text="", font=(
        "Courier", 17), bg="LightGreen", fg="black")
    label5.pack(side=tk.TOP)

    def mostrarRes():
        query = combobox.current()
        inicio = str(date.get_date())
        final = str(date2.get_date())
        nombre = str(usuario.get("1.0", 'end-1c'))
        numero = str(combobox2.get())

        if(query == 0):
            ventasSemanales(inicio, final)

        elif(query == 1):
            ventasArtista(inicio, final, numero)

        elif(query == 2):
            ventasGenero(inicio, final, numero)

        elif(query == 3):
            masRep(numero, nombre)

        else:
            print(query)

    campo4 = tk.Frame(records, bg="LightGreen")
    mostrar = tk.Button(campo4, text="Show", font=(
        "Courier", 15), command=mostrarRes)
    mostrar.pack(side=tk.BOTTOM)
    campo4.pack(ipadx=50)

    label6 = tk.Label(records, text="", font=(
        "Courier", 17), bg="LightGreen", fg="black")
    label6.pack(side=tk.TOP)

    records.mainloop()

######################
##### Comisiones #####
######################

def earnings():
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
    try:

        connection = psycopg2.connect(user = "postgres",
                                      password = "123456",
                                      host = "localhost",
                                      port = "5433",
                                      database = "proyecto2")
        cursor = connection.cursor()

        create_table_query = '''SELECT artist.artistname, name, reps, reps-(reps*0.7) as earnings
FROM song INNER JOIN artist ON song.artist = artist.artistid
GROUP BY artist.artistname, name, reps
ORDER BY earnings DESC'''

        cursor.execute(create_table_query)

        result = cursor.fetchall()

        for row in result:
            print("Artist =", row[0])
            print("Song =", row[1])
            print("Reps =", row[2])
            print("Earnings $USD =", row[3])
            print("\n")

        connection.commit()

        #messagebox.showinfo(message=result, title="Consulta")
    except (Exception, psycopg2.DatabaseError) as error:
        messagebox.showerror(
            message="No se encontro el producto.", title="Consulta fallida")
        print("No se pudo realizar lo solicitado", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")