import flet as ft
import sqlite3
import sys
import os
import pyAesCrypt

conn = sqlite3.connect('notes.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT
    )
''')

class Task(ft.UserControl):
    def __init__(self, task_name, task_text, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_text = task_text
        self.task_status_change = task_status_change
        self.task_delete = task_delete


    def build(self):
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name + " " + self.task_text, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Редактирование заметки",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Удалить заметку",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )
        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip= "Обновить заметку",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    async def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        await self.update_async()

    async def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        await self.update_async()

    async def status_changed(self, e):
        self.completed = self.display_task.value
        await self.task_status_change(self)

    async def delete_clicked(self, e):
        await self.task_delete(self)


class TodoApp(ft.UserControl):
    def build(self):

        self.new_task = ft.TextField(
            hint_text="Введите название заметки", on_submit=self.add_clicked, expand=True
        )
        self.new_task_text = ft.TextField(
            hint_text="Введите текст заметки", on_submit=self.add_clicked, expand=True
        )

        self.tasks = ft.Column()
        self.db_connection()
        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="Все"), ft.Tab(text="Активные"), ft.Tab(text="Выполненные")],
        )

        self.items_left = ft.Text("0 активных")

        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(value="Заметки", style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        self.new_task_text,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text="Удалить заметки", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    async def add_clicked(self, e):

        if self.new_task.value:
            cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (self.new_task.value, self.new_task_text.value))
            conn.commit()
            task = Task(self.new_task.value, self.new_task_text.value, self.task_status_change, self.task_delete)
            self.new_task.value = ""
            self.new_task_text.value = ""
            self.tasks.controls.append(task)
            await self.new_task.focus_async()
            await self.update_async()
            await self.update_async()

    async def task_status_change(self, task):
        await self.update_async()

    async def task_delete(self, task):
        self.db_delete(task)
        self.tasks.controls.remove(task)
        await self.update_async()

    async def tabs_changed(self, e):
        await self.update_async()

    async def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.db_delete(task)
                await self.task_delete(task)

    def db_delete(self, task):
        text = task.task_text
        name = task.task_name
        cursor.execute("DELETE FROM notes WHERE (title, content)=(?,?)", (name, text))
        conn.commit()

    def db_connection(self):
        cursor.execute('SELECT * FROM notes')
        notes = cursor.fetchall()
        for note in notes:
            task = Task(note[1], note[2], self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)

    async def update_async(self):

        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "Все"
                or (status == "Активные" and task.completed == False)
                or (status == "Выполненные" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} активных"
        await super().update_async()

async def main(page: ft.Page): 
    page.title = "Заметки"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    await page.add_async(TodoApp())