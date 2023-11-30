import flet as ft
from random import randint
import subprocess
import hashlib
import pyAesCrypt
import os
import sqlite3
import json


#Decryption file
def decrypt(lo, pa):
    pyAesCrypt.decryptFile(str(lo) + ".db.aes", str(lo) + ".db", pa.value)
    os.remove(str(lo) + ".db.aes")

#Create new user, random salt
def new_usr(pasword):
    salt = str(randint(100000, 999999))
    pas = str(pasword) + salt 
    pas_bytes = pas.encode('utf-8')
    hesh = hashlib.sha512(pas_bytes)
    return hesh.hexdigest(), salt

#Authoriz user
def get_log(password, login):
    salt = ""
    Hash = ""
    with sqlite3.connect('us.db') as conn:
        curs = conn.cursor()
        curs.execute('SELECT * FROM users')
        notes = curs.fetchall()
        for note in notes:
            if note[1] == login:
                salt = note[2]
                Hash = note[3]
    pas = str(password.value) + salt 
    pas_bytes = pas.encode('utf-8')
    hesh = hashlib.sha512(pas_bytes)
    if hesh.hexdigest() == Hash:
        decrypt(login, password)
        return True


def main(page: ft.Page):
        login_txt = ft.TextField(label="Логин", width= 400, autofocus=True)
        password = ft.TextField(label="Пароль", width= 400, password=True)
        greetings = ft.Column()
        page.window_width = 400  
        page.window_height = 400  
        page.window_resizable = False  
        page.update()

        #Registration button
        def reg_button(e):
            log = login_txt.value
            hashe, salt = new_usr(password.value)
            p = password.value
            with sqlite3.connect('us.db') as conn:
                curs = conn.cursor()
                curs.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        user TEXT,
                        salt TEXT,
                        hesh TEXT
                    )
                ''')
                
                curs.execute('SELECT * FROM users')
                notes = curs.fetchall()
                if notes != []:
                        for note in notes:
                            if note[1] == log:
                                print("Юзер есть, ты еблан?")
                            
                        curs.execute('INSERT INTO users (user, hesh, salt) VALUES (?, ?, ?)', (str(log), str(hashe), str(salt)))
                        conn.commit()
                        page.remove(button3)
                        page.add(button1, button2)
                        login_txt.value = ""
                        password.value = ""
                                
                else:
                    curs.execute('INSERT INTO users (user, hesh, salt) VALUES (?, ?, ?)', (str(log), str(hashe), str(salt)))
                    conn.commit()
                    page.remove(button3)
                    page.add(button1, button2)
                    login_txt.value = ""
                    password.value = ""    
            
            with sqlite3.connect(str(log) + '.db') as conn:
                curs = conn.cursor()
                curs.execute('''
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        content TEXT
                    )
                ''')
                pyAesCrypt.encryptFile(str(log) + ".db", str(log) + ".db.aes", p)
            conn.close()
            os.remove(str(log) + ".db")
            page.update()
            
        #Authorize button
        def btn_click(e):
            if get_log(password, login_txt.value) == True:
                page.window_destroy()
                data = {
                    "login": login_txt.value,
                    "password": password.value
                }
                # Запись данных в JSON файл
                with open('credentials.json', 'w') as file:
                    json.dump(data, file)
                subprocess.run(["python", "main.py"])
                page.remove(page)
            login_txt.value = ""
            password.value = ""
            page.update()
            password.focus()
        
        #Reg text button
        def on_text_button_click(e):
            page.remove(button1, button2)
            page.add(button3)
            

        button1 = ft.ElevatedButton("Войти", on_click=btn_click)
        button2 = ft.TextButton("Регистрация", on_click=on_text_button_click)
        button3 = ft.ElevatedButton("Регистрация", on_click=reg_button)
        page.add(login_txt, 
                 password, 
                 button1,
                 button2, 
                 greetings,
                 )
        
        
if __name__ == "__main__":
    ft.app(target=main)