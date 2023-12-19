import flet as ft  # Импорт библиотеки для создания графического интерфейса
from random import randint  # Импорт функции для генерации случайных чисел
import subprocess  # Импорт модуля для запуска внешних процессов
import hashlib  # Импорт модуля для работы с хэшированием
import pyAesCrypt  # Импорт модуля для работы с шифрованием
import os  # Импорт модуля для работы с операционной системой
import sqlite3  # Импорт модуля для работы с базой данных SQLite
import json  # Импорт модуля для работы с JSON


# Расшифровка файла
def decrypt(lo, pa):
    pyAesCrypt.decryptFile(
        str(lo) + ".db.aes", str(lo) + ".db", pa.value
    )  # Расшифровка файла
    os.remove(str(lo) + ".db.aes")  # Удаление зашифрованного файла


# Создание нового пользователя с случайной солью
def new_usr(pasword):
    salt = str(randint(100000, 999999))  # Генерация случайной соли
    pas = str(pasword) + salt  # Конкатенация пароля и соли
    pas_bytes = pas.encode("utf-8")  # Преобразование в байтовую строку
    hesh = hashlib.sha512(pas_bytes)  # Хеширование пароля с солью
    return hesh.hexdigest(), salt  # Возврат хеша пароля и соли


# Авторизация пользователя
def get_log(password, login):
    salt = ""
    Hash = ""
    with sqlite3.connect("us.db") as conn:  # Установление соединения с базой данных
        curs = conn.cursor()  # Создание объекта курсора
        curs.execute("SELECT * FROM users")  # Выполнение SQL-запроса
        notes = curs.fetchall()  # Получение результатов запроса
        for note in notes:
            if note[1] == login:  # Поиск пользователя по логину
                salt = note[2]  # Получение соли из базы данных
                Hash = note[3]  # Получение хеша пароля из базы данных
    pas = str(password.value) + salt  # Конкатенация введенного пароля и соли
    pas_bytes = pas.encode("utf-8")  # Преобразование в байтовую строку
    hesh = hashlib.sha512(pas_bytes)  # Хеширование введенного пароля с солью
    if hesh.hexdigest() == Hash:  # Сравнение полученного хеша с хешем из базы данных
        decrypt(login, password)  # Расшифровка файла
        return True  # Возврат значения True в случае успешной авторизации


def main(page: ft.Page):
    login_txt = ft.TextField(
        label="Логин", width=400, autofocus=True
    )  # Создание текстового поля для ввода логина
    password = ft.TextField(
        label="Пароль", width=400, password=True
    )  # Создание текстового поля для ввода пароля
    greetings = ft.Column()  # Создание блока для приветствия пользователя
    page.window_width = 400  # Установка ширины окна
    page.window_height = 400  # Установка высоты окна
    page.window_resizable = False  # Запрет изменения размеров окна

    page.update()  # Обновление графического интерфейса

    # Обработчик кнопки "Регистрация"
    def reg_button(e):
        b = False  # Флаг для проверки существования пользователя
        log = login_txt.value  # Получение введенного логина
        hashe, salt = new_usr(password.value)  # Создание хеша пароля и соли
        p = password.value  # Получение введенного пароля
        with sqlite3.connect("us.db") as conn:  # Установление соединения с базой данных
            curs = conn.cursor()  # Создание объекта курсора
            curs.execute(
                """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        user TEXT,
                        salt TEXT,
                        hesh TEXT
                    )
                """
            )  # Создание таблицы пользователей, если она не существует

            curs.execute("SELECT * FROM users")  # Выполнение SQL-запроса
            notes = curs.fetchall()  # Получение результатов запроса
            if notes != []:  # Проверка наличия пользователей в базе данных
                for note in notes:
                    if note[1] == log:  # Поиск пользователя с таким логином
                        page.add(text)  # Добавление текста об ошибке
                        b = True  # Установка флага в True
                        return  # Выход из функции
                if b == True:  # Если пользователь существует
                    page.remove(text)  # Удаление текста об ошибке
                curs.execute(
                    "INSERT INTO users (user, hesh, salt) VALUES (?, ?, ?)",
                    (str(log), str(hashe), str(salt)),
                )  # Добавление нового пользователя в базу данных
                conn.commit()  # Фиксация изменений в базе данных
                page.remove(button3)  # Удаление кнопки "Регистрация"
                page.add(button1, button2)  # Добавление кнопок "Войти" и "Регистрация"
                login_txt.value = ""  # Очистка поля ввода логина
                password.value = ""  # Очистка поля ввода пароля

            else:  # Если база данных пуста
                curs.execute(
                    "INSERT INTO users (user, hesh, salt) VALUES (?, ?, ?)",
                    (str(log), str(hashe), str(salt)),
                )  # Добавление нового пользователя в базу данных
                conn.commit()  # Фиксация изменений в базе данных
                page.remove(button3)  # Удаление кнопки "Регистрация"
                page.add(button1, button2)  # Добавление кнопок "Войти" и "Регистрация"
                login_txt.value = ""  # Очистка поля ввода логина
                password.value = ""  # Очистка поля ввода пароля
        conn.close()  # Закрытие соединения с базой данных
        with sqlite3.connect(
            str(log) + ".db"
        ) as conn:  # Установление соединения с базой данных
            curs = conn.cursor()  # Создание объекта курсора
            curs.execute(
                """
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        content TEXT
                    )
                """
            )  # Создание таблицы для заметок пользователя
            pyAesCrypt.encryptFile(
                str(log) + ".db", str(log) + ".db.aes", p
            )  # Шифрование файла
        conn.close()  # Закрытие соединения с базой данных
        os.remove(str(log) + ".db")  # Удаление исходного файла
        page.update()  # Обновление графического интерфейса

    # Обработчик кнопки "Войти"
    def btn_click(e):
        if (
            get_log(password, login_txt.value) == True
        ):  # Если авторизация прошла успешно
            page.window_destroy()  # Закрытие окна
            data = {
                "login": login_txt.value,  # Логин пользователя
                "password": password.value,  # Пароль пользователя
            }
            # Запись данных в JSON файл
            with open("credentials.json", "w") as file:
                json.dump(data, file)
            subprocess.run(["python", "main.py"])  # Запуск основной программы
            page.remove(page)  # Удаление элементов графического интерфейса
        login_txt.value = ""  # Очистка поля ввода логина
        password.value = ""  # Очистка поля ввода пароля
        page.update()  # Обновление графического интерфейса
        password.focus()  # Установка фокуса на поле ввода пароля

    # Обработчик кнопки "Регистрация"
    def on_text_button_click(e):
        page.remove(button1, button2)  # Удаление кнопок "Войти" и "Регистрация"
        page.add(button3)  # Добавление кнопки "Регистрация"

    button1 = ft.ElevatedButton("Войти", on_click=btn_click)  # Создание кнопки "Войти"
    button2 = ft.TextButton(
        "Регистрация", on_click=on_text_button_click
    )  # Создание кнопки "Регистрация"
    text = ft.Text("Такой пользователь уже существует")  # Создание текста об ошибке
    button3 = ft.ElevatedButton(
        "Регистрация", on_click=reg_button
    )  # Создание кнопки "Регистрация"
    page.add(
        login_txt,
        password,
        button1,
        button2,
        greetings,
    )  # Добавление элементов на страницу


if __name__ == "__main__":
    ft.app(target=main)  # Запуск графического интерфейса
