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
    arg = input('\n Reports: \n 1. Most recent albums \n 2. Most popular artist \n 3. New users \n 4. Artist with more tracks \n 5. Most popular genres \n 6. Most active users \n 7.')
    arg = int(arg)
    if arg == 1:
        try:
            cur.execute('''SELECT name, release_date FROM album  WHERE release_date > '2021-03-20' ORDER BY release_date DESC limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")

    elif arg == 2:
        try:
            cur.execute('''SELECT artistname as name FROM artist  INNER JOIN song ON song.artist = artistid GROUP BY artistname ORDER BY sum(song.reps) LIMIT 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")

    elif arg == 3:
        try:
            cur.execute('''SELECT count(subdate) as name FROM users WHERE subdate > '2020-09-01' limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")
            
    elif arg == 4:
        try:
            cur.execute('''SELECT artist.artistname as name, count(artist.artistname) FROM song INNER JOIN artist ON song.artist = artist.artistid GROUP BY artistname ORDER BY count DESC limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")
            
    elif arg == 5:
        try:
            cur.execute('''SELECT  genre as name FROM song GROUP BY genre order BY count(*) DESC limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")
            
    elif arg == 6:
        try:
            cur.execute('''SELECT mail as name, plays FROM users order BY plays DESC limit 3''', (arg,))
            res = cur.fetchall()
            conn.commit()
        except:
            conn.rollback()
            print("Error, something went wrong with the connection")
     
    else:
        print('bruh')

############################
######  REPORTERIA 2   #####
############################

def ventasSemanales(inicio, final):
        try:  
        
            connection = psycopg2.connect(user = "postgres",
                                          password = "pw4pg",
                                          host = "localhost",
                                          port = "5432",
                                          database = "proyecto2")
            cursor = connection.cursor()
            
            create_table_query = ''''''

            cursor.execute(create_table_query)

            result = cursor.fetchall()
            
            connection.commit()                 
            
            messagebox.showinfo(message=result, title="Consulta")
        except (Exception, psycopg2.DatabaseError) as error :
            messagebox.showerror(message="No se encontro el producto.", title="Consulta fallida")
            print ("No se pudo realizar lo solicitado", error)
            
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")

def ventasArtista(inicio, final, cantidad):
        try:  
        
            connection = psycopg2.connect(user = "postgres",
                                          password = "pw4pg",
                                          host = "localhost",
                                          port = "5432",
                                          database = "proyecto2")
            cursor = connection.cursor()
            
            create_table_query = ''''''
            
            cursor.execute(create_table_query)

            result = cursor.fetchall()

            for row in result:
                print("Fecha =", row[0])
                print("Artista =", row[1])
                print("Id Cancion =", row[2])
                print("Total Totales =" , row[3], "\n")
            
            connection.commit()                 
            
            messagebox.showinfo(message=result, title="Consulta")
        except (Exception, psycopg2.DatabaseError) as error :
            messagebox.showerror(message="No se encontro el producto.", title="Consulta fallida")
            print ("No se pudo realizar lo solicitado", error)
            
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")

def ventasGenero(inicio, final, cantidad):
        try:  
        
            connection = psycopg2.connect(user = "postgres",
                                          password = "pw4pg",
                                          host = "localhost",
                                          port = "5432",
                                          database = "proyecto2")
            cursor = connection.cursor()
            
            create_table_query = ''''''
            
            cursor.execute(create_table_query)

            result = cursor.fetchall()

            for row in result:
                print("Fecha =", row[0])
                print("Genero =", row[1])
                print("Id Cancion =", row[2])
                print("Total Ventas =" , row[3], "\n")
            
            connection.commit()                 
            
            messagebox.showinfo(message=result, title="Consulta")
        except (Exception, psycopg2.DatabaseError) as error :
            messagebox.showerror(message="No se encontro el producto.", title="Consulta fallida")
            print ("No se pudo realizar lo solicitado", error)
            
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")

def masRep(cantidad, artista):
        try:  
        
            connection = psycopg2.connect(user = "postgres",
                                          password = "pw4pg",
                                          host = "localhost",
                                          port = "5432",
                                          database = "proyecto2")
            cursor = connection.cursor()
            
            create_table_query = ''''''
            
            cursor.execute(create_table_query)

            result = cursor.fetchall()

            for row in result:
                print("Artista =", row[0])
                print("Nombre de la cancion =" , row[1])
                print("Numero de reproducciones =", row[2])
                
                
            
            connection.commit()                 
            
            messagebox.showinfo(message=result, title="Consulta")
        except (Exception, psycopg2.DatabaseError) as error :
            messagebox.showerror(message="No se encontro el producto.", title="Consulta fallida")
            print ("No se pudo realizar lo solicitado", error)
            
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")

#######################
### Ventana grafica ###
#######################
def ventanaRecords():

    values = ["Total sales", "Top sales in artists", "Top sales by musical genre", "Most listened tracks by an artist"]
    
    def q1():
        date.configure(state = "readonly")
        date2. configure(state = "readonly")
        usuario.configure(state = "disabled")
        combobox2.configure(state = "disabled")
        
    def q2():
        date.configure(state = "readonly")
        date2. configure(state = "readonly")
        usuario.configure(state = "disabled")
        combobox2.configure(state = "readonly")
    def q3():
        date.configure(state = "readonly")
        date2. configure(state = "readonly")
        usuario.configure(state = "disabled")
        combobox2.configure(state = "readonly")
    def q4():
        date.configure(state = "disabled")
        date2. configure(state = "disabled")
        usuario.configure(state = "normal")
        combobox2.configure(state = "readonly")
        
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
    records.configure(background = "LightGreen")

    label1= tk.Label(records, text="Records", font=("Century", 44), pady=40, bg="LightGreen", fg="black")
    label1.pack()

    campo1 = tk.Frame(records, bg = "LightGreen")
    
    label1 = tk.Label(campo1, text="Record:", font=("Courier", 20), bg="LightGreen", fg="black")
    label1.pack(side=tk.TOP)

    combobox = ttk.Combobox(campo1, width=50, values = ["Total sales", "Top sales in artists", "Top sales by musical genre", "Most listened tracks by an artist"], state='readonly')
    combobox.bind("<<ComboboxSelected>>", handler)
    combobox.pack(side = tk.BOTTOM)
    combobox.current(0)
    
    campo1.pack(side=tk.TOP)

    

    label4 = tk.Label(records, text="", font=("Courier", 17), bg="LightGreen", fg="black")
    label4.pack(side=tk.TOP)

    
    
    campo2 = tk.Frame(records, bg = "LightGreen")
    label2 = tk.Label(campo2, text="Date:", font=("Courier", 17), bg="LightGreen", fg="black")
    label2.pack(side=tk.TOP)
    
    label2 = tk.Label(campo2, text="Initiation:", font=("Courier", 13), bg="LightGreen", fg="black")
    label2.pack(side=tk.LEFT, ipady = 7)
    
    date = DateEntry(campo2, background='darkblue', foreground='white', year=2020, state='readonly' )
    date.pack(side = tk.LEFT)
    
    label3 = tk.Label(campo2, text="     End:", font=("Courier", 13), bg="LightGreen", fg="black")
    label3.pack(side=tk.LEFT, ipady = 7)
    
    date2 = DateEntry(campo2, background='darkblue', foreground='white', year=2020, state='readonly')
    date2.pack(side = tk.LEFT)

    campo2.pack(side=tk.TOP)


    label4 = tk.Label(records, text="", font=("Courier", 17), bg="LightGreen", fg="black")
    label4.pack(side=tk.TOP)


    campo3 = tk.Frame(records, bg = "LightGreen")

    label4 = tk.Label(campo3, text="Complete information:", font=("Courier", 17), bg="LightGreen", fg="black")
    label4.pack(side=tk.TOP)

    label5 = tk.Label(campo3, text="Artist:", font=("Courier", 13), bg="LightGreen", fg="black")
    label5.pack(side=tk.LEFT, ipady = 7)

    usuario = tk.Text(campo3, width=12, height=1, state = "disabled")
    usuario.pack(side = tk.LEFT)

    label6 = tk.Label(campo3, text="   Amount:", font=("Courier", 13), bg="LightGreen", fg="black")
    label6.pack(side=tk.LEFT, ipady = 7)

    combobox2 = ttk.Combobox(campo3, width=10, values = [10, 7, 5, 1], state='disabled')
    combobox2.pack(side = tk.LEFT)
    combobox2.current(0)
    
    campo3.pack(side=tk.TOP)

    label5 = tk.Label(records, text="", font=("Courier", 17), bg="LightGreen", fg="black")
    label5.pack(side=tk.TOP)

    def mostrarRes():
        query = combobox.current()
        inicio = str(date.get_date())
        final = str(date2.get_date())
        nombre = str(usuario.get("1.0",'end-1c'))
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

    
    campo4 = tk.Frame(records, bg = "LightGreen") 
    mostrar = tk.Button(campo4, text = "Show", font=("Courier", 15), command=mostrarRes)
    mostrar.pack(side=tk.BOTTOM)
    campo4.pack(ipadx = 50)

    label6 = tk.Label(records, text="", font=("Courier", 17), bg="LightGreen", fg="black")
    label6.pack(side=tk.TOP)

    records.mainloop()
ventanaRecords()

