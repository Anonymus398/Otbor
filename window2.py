import flet as ft

def main(page: ft.Page):

        login_txt = ft.TextField(label="Логин", width= 400, autofocus=True)
        password = ft.TextField(label="Пароль", width= 400)
        greetings = ft.Column()
        User = "Admin"
        Password = "123456"
        page.window_width = 400  # window's width is 200 px
        page.window_height = 400  # window's height is 200 px
        page.window_resizable = False  # window is not resizable
        page.update()

        def btn_click(e):
            if str(login_txt.value) == User and str(password.value) == Password:
                print("Hello")
            login_txt.value = ""
            password.value = ""
            page.update()
            password.focus()
        
        page.add(
            login_txt,
            password,
            ft.ElevatedButton("Войти", on_click=btn_click),
            greetings,
        )
        
if __name__ == "__main__":
    ft.app(target=main)