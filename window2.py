import flet as ft
import subprocess
import hashlib

#Create new user
def new_usr(pasword):
    salt = "51812910"
    pas = str(pasword) + salt 
    pas_bytes = pas.encode('utf-8')
    hesh = hashlib.sha512(pas_bytes)
    return hesh.hexdigest()


def get_log(password):
    salt = "518129"
    Hash = "0b602f0fb5988dd2fd08e2aedef82760e1d5f3438c95fc5edfb4da752c81ac9fecd70a1f399ffbf5e172351c1745fcbc76233930f73fe17f5a7c89b55fb4ea58"
    pas = str(password.value) + salt 
    pas_bytes = pas.encode('utf-8')
    hesh = hashlib.sha512(pas_bytes)
    if hesh.hexdigest() == Hash:
        return True


def main(page: ft.Page):
        login_txt = ft.TextField(label="Логин", width= 400, autofocus=True)
        password = ft.TextField(label="Пароль", width= 400)
        greetings = ft.Column()
        User = "Admin"
        page.window_width = 400  
        page.window_height = 400  
        page.window_resizable = False  
        page.update()
        
        def reg_button(e):
            log = login_txt.value
            pas = new_usr(password.value)
            page.remove(button3)
            page.add(button1, button2)
            login_txt.value = ""
            password.value = ""
            page.update()
            password.focus()
            print(log)
            print(pas)
            

        def btn_click(e):
            if str(login_txt.value) == User and get_log(password) == True:
                page.window_destroy()
                subprocess.run(["python", "main.py"])
            login_txt.value = ""
            password.value = ""
            page.update()
            password.focus()

        def on_text_button_click(e):
            page.remove(button1, button2)
            page.add(button3)
            #page.remove_all() 

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