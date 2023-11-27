import flet as ft
import subprocess

def main(page: ft.Page):
        login_txt = ft.TextField(label="Логин", width= 400, autofocus=True)
        password = ft.TextField(label="Пароль", width= 400)
        greetings = ft.Column()
        User = "Admin"
        Password = "123456"
        page.window_width = 400  
        page.window_height = 400  
        page.window_resizable = False  
        page.update()
        def btn_click(e):
            if str(login_txt.value) == User and str(password.value) == Password:
                page.window_destroy()
                subprocess.run(["python", "main.py"])
            login_txt.value = ""
            password.value = ""
            page.update()
            password.focus()
        page.add(login_txt, password, ft.ElevatedButton("Войти", on_click=btn_click), greetings,)
        
if __name__ == "__main__":
    ft.app(target=main)