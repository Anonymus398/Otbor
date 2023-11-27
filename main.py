import flet as ft
from window import TodoApp


async def main(page: ft.Page): 
    page.title = "Заметки"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    await page.add_async(TodoApp())

if __name__ == "__main__":
    ft.app(target=main)