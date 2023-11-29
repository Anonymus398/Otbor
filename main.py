import flet as ft
from window import TodoApp, conn
from window2 import pac, lo
import pyAesCrypt
import os
import sys


def encrypt(pac, lo):
    pyAesCrypt.encryptFile(str(lo) + ".db", str(lo) + ".db.aes", pac)
    conn.close()
    os.remove(str(lo) + ".db")


async def main(page: ft.Page): 
    page.title = "Заметки"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    await page.add_async(TodoApp())

if __name__ == "__main__":
    ft.app(target=main)
sys.exit(encrypt(pac, lo))
