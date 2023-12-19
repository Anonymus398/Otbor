import flet as ft  # Импорт модуля flet под псевдонимом ft
from window import TodoApp, conn  # Импорт классов TodoApp и conn из модуля window
import pyAesCrypt  # Импорт модуля pyAesCrypt
import os  # Импорт модуля os
import sys  # Импорт модуля sys
import json  # Импорт модуля json

with open(
    "credentials.json", "r"
) as file:  # Открытие файла credentials.json в режиме чтения
    data = json.load(file)  # Загрузка данных из файла в формате JSON
    login = data["login"]  # Извлечение логина из данных
    password = data["password"]  # Извлечение пароля из данных


def encrypt(pac, lo):  # Определение функции encrypt с параметрами pac и lo
    pyAesCrypt.encryptFile(
        str(lo) + ".db", str(lo) + ".db.aes", pac
    )  # Шифрование файла
    conn.close()  # Закрытие соединения
    os.remove(str(lo) + ".db")  # Удаление исходного файла


async def main(page: ft.Page):  # Определение асинхронной функции main с параметром page
    page.title = "Заметки"  # Установка заголовка страницы
    page.horizontal_alignment = (
        ft.CrossAxisAlignment.CENTER
    )  # Установка горизонтального выравнивания
    page.scroll = ft.ScrollMode.ADAPTIVE  # Установка режима прокрутки
    await page.add_async(
        TodoApp()
    )  # Асинхронное добавление объекта TodoApp на страницу


if __name__ == "__main__":  # Проверка, что скрипт запущен как отдельное приложение
    os.remove("credentials.json")  # Удаление файла credentials.json
    ft.app(target=main)  # Запуск приложения с функцией main в качестве цели
sys.exit(encrypt(password, login))  # Выход из программы после шифрования данных