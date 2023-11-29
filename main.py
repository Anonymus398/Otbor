import flet as ft
from window import TodoApp, conn
import pyAesCrypt
import os
import sys
password = "123456"
def encrypt(password):
    pyAesCrypt.encryptFile("notes.db", "notes.db.aes", password)
    conn.close()
    os.remove("notes.db")


async def main(page: ft.Page): 
    page.title = "Заметки"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    await page.add_async(TodoApp())

if __name__ == "__main__":
    ft.app(target=main)
sys.exit(encrypt(password))