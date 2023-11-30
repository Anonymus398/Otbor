import flet as ft
from window import TodoApp, conn
import pyAesCrypt
import os
import sys
import json

with open('credentials.json', 'r') as file:
    data = json.load(file)
    login = data["login"]
    password = data["password"]

def encrypt(pac, lo):
    pyAesCrypt.encryptFile(str(lo) + ".db", str(lo) + ".db.aes", pac)
    conn.close()
    os.remove(str(lo) + ".db")
    os.remove('credentials.json')


async def main(page: ft.Page): 
    page.title = "Заметки"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    await page.add_async(TodoApp())

if __name__ == "__main__":
    ft.app(target=main)
sys.exit(encrypt(password, login))
