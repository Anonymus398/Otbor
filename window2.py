import flet as ft
from random import randint
import subprocess
import hashlib
import pyAesCrypt
import os
import sqlite3


#Decryption file
def decrypt(password):
    pyAesCrypt.decryptFile("notes.db.aes", "notes.db", password.value)
    os.remove("notes.db.aes")

#Create new user, random salt
def new_usr(pasword):
    salt = str(randint(100000, 999999))
    pas = str(pasword) + salt 
    pas_bytes = pas.encode('utf-8')
    hesh = hashlib.sha512(pas_bytes)
    return hesh.hexdigest(), salt

#Authoriz user
def get_log(password):
    salt = "518129"
    Hash = "0b602f0fb5988dd2fd08e2aedef82760e1d5f3438c95fc5edfb4da752c81ac9fecd70a1f399ffbf5e172351c1745fcbc76233930f73fe17f5a7c89b55fb4ea58"
    pas = str(password.value) + salt 
    pas_bytes = pas.encode('utf-8')
    hesh = hashlib.sha512(pas_bytes)
    if hesh.hexdigest() == Hash:
        decrypt(password)
        return True


def main(page: ft.Page):
        login_txt = ft.TextField(label="Логин", width= 400, autofocus=True)
        password = ft.TextField(label="Пароль", width= 400, password=True)
        greetings = ft.Column()
        User = "Admin"
        page.window_width = 400  
        page.window_height = 400  
        page.window_resizable = False  
        page.update()

        #Registration button
        def reg_button(e):
            log = login_txt.value
            hashe, salt = new_usr(password.value)
            page.remove(button3)
            page.add(button1, button2)
            login_txt.value = ""
            password.value = ""
            page.update()
            password.focus()
            with sqlite3.connect('us.db') as conn:
                curs = conn.cursor()
                curs.execute('INSERT INTO users (user, hesh, salt) VALUES (?, ?, ?)', (str(log), str(hashe), str(salt)))
                conn.commit()
            
        #Authorize button
        def btn_click(e):
            if str(login_txt.value) == User and get_log(password) == True:
                page.window_destroy()
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