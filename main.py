"""
Модуль является одновременно и точкой входа, и содержит оснвные функции, отвечающие
за графический интефейс
"""
import tkinter as tk
from typing import List, Dict, Any
from tkinter import messagebox
from pandastable import Table

import general_comands as gc
import help_text


def show_help(window: Any) -> None:
    """
    Создает окно и отображате документацию приложения.

    Parameters
    ----------
    window : Any
        Объект tk.Tk() основного окна приложения

    Returns
    -------
    None
    """
    new_window = tk.Toplevel(window)
    new_window.title("Помощь")
    new_window.geometry('500x400+300+100')

    quote: str = help_text.text
    scroll = tk.Scrollbar(new_window)
    text = tk.Text(new_window, font="clearlyu 15")
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text.pack(side=tk.LEFT, fill=tk.Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    text.insert(tk.END, quote)


def on_closing(window: Any) -> None:
    """
    Закрывает окно

    Parameters
    ----------
    window : Any
        Объект tk.Tk() основного окна приложения

    Returns
    -------
    None
    """
    if messagebox.askokcancel("Quit", "Вы точно хотите выйти?"): 
        window.destroy()


def add_window(window: Any) -> None:
    """
    Открывает окно добавления новой книги в библиотеку
    При нажатии на кнопку "Сохранить изменения" вызывается функция edit_command из модуля general_comands.
    Она обновляет библиотеку, перезаписывая файл lib.json

    Parameters
    ----------
    window : Any
        Объект tk.Tk() основного окна приложения

    Returns
    -------
    None
    """
    # Подгружем библиотеку
    data: List[Dict] = gc.load_data_form_json()

    new_window = tk.Toplevel(window)
    new_window.title("Добавление книги")
    new_window.geometry('400x300+300+100')

    title_text = tk.StringVar()
    author_text = tk.StringVar()
    pages_text = tk.StringVar()
    year_text = tk.StringVar()
    rating_text = tk.StringVar()

    nw_l1 = tk.Label(new_window, text="Информация о книге", font="clearlyu 15", )
    nw_l1.grid(row=0, column=1)

    nw_l3 = tk.Label(new_window, text="Название", font="clearlyu 13", )
    nw_l3.grid(row=4, column=0)
    nw_e3 = tk.Entry(new_window, textvariable=title_text)
    nw_e3.grid(row=4, column=1)

    nw_l4 = tk.Label(new_window, text="Автор", font="clearlyu 13", )
    nw_l4.grid(row=6, column=0)
    nw_e4 = tk.Entry(new_window, textvariable=author_text)
    nw_e4.grid(row=6, column=1)

    nw_l5 = tk.Label(new_window, text="Рейтинг", font="clearlyu 13", )
    nw_l5.grid(row=8, column=0)
    nw_e5 = tk.Entry(new_window, textvariable=rating_text)
    nw_e5.grid(row=8, column=1)

    nw_l6 = tk.Label(new_window, text="Кол-во страниц", font="clearlyu 13", )
    nw_l6.grid(row=10, column=0)
    nw_e6 = tk.Entry(new_window, textvariable=pages_text)
    nw_e6.grid(row=10, column=1)

    nw_l7 = tk.Label(new_window, text="Год выпуска", font="clearlyu 13", )
    nw_l7.grid(row=12, column=0)
    nw_e7 = tk.Entry(new_window, textvariable=year_text)
    nw_e7.grid(row=12, column=1)

    nw_b8 = tk.Button(new_window, text="Сохранить изменения", width=20, bg='green', font="clearlyu 13",
                      command=lambda: gc.edit_command(data, nw_e3, nw_e4, nw_e5, nw_e6, nw_e7, id=None))
    nw_b8.grid(row=16, column=1)


def create_window(input_id: int, window: Any) -> None:
    """
    Открывает окно редактирования существующей книги в библиотеке
    При нажатии на кнопку "Сохранить изменения" вызывается функция edit_command из модуля general_comands.
    Она обновляет библиотеку, перезаписывая файл lib.json

    Parameters
    ----------
    input_id: int - идентикафиционный номер в книге
    window: Any
        Объект tk.Tk() основного окна приложения

    Returns
    -------
    None
    """
    if not input_id:
        messagebox.showinfo("Редактирование", "Вы не ввели id")
        return None
    elif not str(input_id).isdigit():
        messagebox.showinfo("Редактирование", "Введите число!")
        return None

    data: List[Dict] = gc.load_data_form_json()

    for index, book in enumerate(data):
        if book['id'] == int(input_id):
            id_title, id_author = str(book['title']), ', '.join(book['author']),
            id_year, id_pages, id_rating = str(book['year']), str(book['pages']), str(book['rating']),
            break
    else:
        messagebox.showinfo("Редактирование", "Нет такого id")
        return None

    new_window = tk.Toplevel(window)
    new_window.title("Редактирование книги")
    new_window.geometry('400x300+300+100')

    title_text = tk.StringVar()
    author_text = tk.StringVar() 
    pages_text = tk.StringVar()
    year_text = tk.StringVar()
    rating_text = tk.StringVar()

    nw_l1 = tk.Label(new_window, text="Информация о книге", font="clearlyu 15",) 
    nw_l1.grid(row=0, column=1)

    nw_l3 = tk.Label(new_window, text="Название", font="clearlyu 13",)
    nw_l3.grid(row=4, column=0)
    nw_e3 = tk.Entry(new_window, textvariable=title_text)
    nw_e3.grid(row=4, column=1)
    nw_e3.insert(0, id_title)

    nw_l4 = tk.Label(new_window, text="Автор", font="clearlyu 13",)
    nw_l4.grid(row=6, column=0)
    nw_e4 = tk.Entry(new_window, textvariable=author_text)
    nw_e4.grid(row=6, column=1)
    nw_e4.insert(0, id_author)

    nw_l5 = tk.Label(new_window, text="Рейтинг", font="clearlyu 13", )
    nw_l5.grid(row=8, column=0)
    nw_e5 = tk.Entry(new_window, textvariable=rating_text)
    nw_e5.grid(row=8, column=1)
    nw_e5.insert(0, id_rating)

    nw_l6 = tk.Label(new_window, text="Кол-во страниц", font="clearlyu 13",)
    nw_l6.grid(row=10, column=0)
    nw_e6 = tk.Entry(new_window, textvariable=pages_text)
    nw_e6.grid(row=10, column=1)
    nw_e6.insert(0, id_pages)

    nw_l7 = tk.Label(new_window, text="Год выпуска", font="clearlyu 13",)
    nw_l7.grid(row=12, column=0)
    nw_e7 = tk.Entry(new_window, textvariable=year_text)
    nw_e7.grid(row=12, column=1)
    nw_e7.insert(0, id_year)

    nw_b8 = tk.Button(new_window, text="Сохранить изменения", width=20, bg='green', font="clearlyu 13",
                      command=lambda: gc.edit_command(data, nw_e3, nw_e4, nw_e5, nw_e6, nw_e7, input_id))
    nw_b8.grid(row=16, column=1)


def show_boo(window: Any) -> None:
    """
    Открывает окно и показывает имеющиеся в библиотеке книги.
    Визуализация происходит с помощью готовой библиотеки pandastable.

    Parameters
    ----------
    window: Any
        Объект tk.Tk() основного окна приложения

    Returns
    -------
    None
    """
    boo_window = tk.Toplevel(window)
    boo_window.geometry('1100x400+200+100')
    boo_window.title('Библиотечная полка')

    frame = tk.Frame(boo_window)
    frame.pack(fill=tk.BOTH, expand=1)
    df = gc.load_json()
    pt = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    pt.autoResizeColumns()
    pt.show()


def gui() -> None:
    """
    Создает основное окно приложения.

    Returns
    -------
    None
    """
    window = tk.Tk()
    window.title("Моя библиотека")
    window.geometry('650x400+300+50')

    mainmenu = tk.Menu(window)
    helpmenu = tk.Menu(mainmenu, tearoff=0)
    helpmenu.add_command(label="Документация", command=lambda: show_help(window))
    mainmenu.add_cascade(label="Помощь", menu=helpmenu)

    title_text = tk.StringVar()
    e1 = tk.Entry(window, textvariable=title_text)
    e1.insert(0, "Название")
    e1.grid(row=4, column=3)

    author_text = tk.StringVar()
    e2 = tk.Entry(window, textvariable=author_text)
    e2.insert(0, "Автор")
    e2.grid(row=1, column=3)

    l4 = tk.Label(window, text="Выберите id:", font="clearlyu 13",)
    l4.grid(row=14, column=0)

    id_text = tk.StringVar()
    e4 = tk.Entry(window, textvariable=id_text)
    e2.insert(0, "")
    e4.grid(row=14, column=1)

    list_text = tk.Label(window, text="Список книг:", font="clearlyu 15",)
    list_text.grid(row=0, column=1)

    search_text = tk.Label(window, text="Поиск:", font="clearlyu 15",)
    search_text.grid(row=0, column=3)

    search_text = tk.Label(window, text="Редактирование:", font="clearlyu 15",)
    search_text.grid(row=4, column=1)

    show_button = tk.Button(window, text="Показать все", width=12,
                            font="clearlyu 13", command=lambda: show_boo(window))
    show_button.grid(row=1, column=1)

    search_a_button = tk.Button(window, text="Поиск по автору", width=17, font="clearlyu 12",
                                command=lambda: gc.search_author(e2.get(), window))
    search_a_button.grid(row=2, column=3)

    search_t_button = tk.Button(window, text="Поиск по названию", width=17, font="clearlyu 12",
                                command=lambda: gc.search_command(e1.get(), 'title', window))
    search_t_button.grid(row=5, column=3)

    delete_button = tk.Button(window, text="Удалить книгу по id", width=20, bg='white',
                              font="clearlyu 13", command=lambda: gc.delete_command(e4.get()))
    delete_button.grid(row=16, column=2)

    quit_button = tk.Button(window, text="Выйти", width=12, bg='red',
                            font="clearlyu 13", command=window.destroy)
    quit_button.grid(row=30, column=3)

    edit_button = tk.Button(window, text="Редактировать по id", width=20, bg='yellow',
                            font="clearlyu 13", command=lambda: create_window(e4.get(), window))
    edit_button.grid(row=16, column=1)

    create_button = tk.Button(window, text="Добавить книгу", width=20, bg='orange', font="clearlyu 13",
                              command=lambda: add_window(window))
    create_button.grid(row=30, column=1)

    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))
    window.config(menu=mainmenu)
    window.mainloop()


if __name__ == '__main__':
    gui()
