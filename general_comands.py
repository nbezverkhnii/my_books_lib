"""
Модель содержит основные команды приложения.
Тут сосредоточены (не почти) функции, которые не затрагивают основной графический интерфейс.
Эта часть задумана, как бэкэнд, хоть и не получилось полностью отвязаться от интерфейся.
"""
import json
import pandas as pd
import tkinter as tk
from typing import List, Dict, Any, Optional
from tkinter import messagebox
from pandastable import Table

import config

DATABASE: str = config.lib_filename


def load_data_form_json() -> List[Dict]:
    """
    Считывает данные из json-файла библиотеки.
    Помещает в список словарей, где каждый словарь - книга.

    Returns
    -------
    data: List[Dict]
        Спсиок словарей, где каждый словварь - книга
    """
    with open(DATABASE) as json_file:
        data = json.load(json_file)

    return data


def load_json():
    """
    Считывает данные из json-файла библиотеки.
    Помещает в pandas DataFrame. Берем только те столбцы, с которыми будем работать.
    Эти столбцы: 'id', 'title', 'author', 'year', 'pages', 'rating'

    Returns
    -------
    data: List[Dict]
        Спсиок словарей, где каждый словварь - книга
    """
    with open(DATABASE) as json_file:
        data = json.load(json_file)
        df = pd.DataFrame.from_dict(data)
        df['author'] = df['author'].apply(lambda x: ', '.join(map(str, x)))
        df.drop(['isbn13'], axis=1, inplace=True)
        titles = list(df.columns)
        titles[0], titles[1], titles[2], titles[3], titles[4], titles[5] = 'id', 'title', 'author', 'year', 'pages', 'rating'
        df = df[titles]

    return df


def edit_command(data: List[Dict],
                 nw_e3: Any,
                 nw_e4: Any,
                 nw_e5: Any,
                 nw_e6: Any,
                 nw_e7: Any,
                 id: Optional[int] = None) -> None:
    """
    Parameters
    ----------
    data: List[Dict]
         Список словарей с нигами
    nw_e3: Any (на самом деле это объект tk.Entry, но я не знаю как его записать в typing)
        Метод get() считает из поля Название книги
    nw_e4: Any (на самом деле это объект tk.Entry, но я не знаю как его записать в typing)
        Метод get() считает из поля Аторов книги
    nw_e5: Any (на самом деле это объект tk.Entry, но я не знаю как его записать в typing)
        Метод get() считает из поля Год книги
    nw_e6: Any (на самом деле это объект tk.Entry, но я не знаю как его записать в typing)
        Метод get() считает из поля Страницы книги
    nw_e7: Any (на самом деле это объект tk.Entry, но я не знаю как его записать в typing)
        Метод get() считает из поля Рейтинг книги
    id: Optional[int]=None

    Returns
    -------
    None
    """
    if id is None:
        id = data[-1]['id'] + 1
        data.append({'id': id})

    for book in data:
        if book['id'] == int(id):
            book['title'] = nw_e3.get()
            book['author'] = nw_e4.get().split(', ')
            book['year'] = int(nw_e7.get())
            book['pages'] = int(nw_e6.get())
            book['rating'] = float(nw_e5.get())

    msg_box = messagebox.askquestion('Изменение', f'Внести изменения?',
                                     icon='warning')
    if msg_box == 'yes':
        with open(DATABASE, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def delete_command(id: int) -> None:
    """
    Удаляет данные из библиотеки (и из файла!) навесгда.
    Пробегает по списку словарей, если находит нужную книгу с нужным id,
    то удалет словарь из списка

    Parameters
    ----------
    id: int
         Идентификационный номер кинги

    Returns
    -------
    None
    """
    if not id:
        messagebox.showinfo("Удаление", "Введите id!")
        return None
    elif not str(id).isdigit():
        messagebox.showinfo("Удаление", "Введите число!")
        return None

    data = load_data_form_json()

    msgbox = messagebox.askquestion('Удаление', f'Вы точно хотите удалить книгу с id={id}',
                                    icon='warning')
    if msgbox == 'yes':
        for index, book in enumerate(data):
            if book['id'] == int(id):
                del data[index]
                break
        with open(DATABASE, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def search_command(value: str, column: str, window: Any) -> None:
    """
    Поиск книги по названиию. Работает методами библиоткеи pandas с DataFrame.
    Выбирает все книги название которых полностью совпадает со значением value.

    Parameters
    ----------
    value: str
        Введенное пользователем занчение названия книги, которе нужно найти
    column: str
        Определяет колонку в pandas DataFrameв которой нужно искать. В данном случает 'title'
    window: Any
        Объект tk.Tk() основного окна приложения

    Returns
    -------
    None
    """
    df = load_json()
    res_df = df[df[column] == value]

    if not len(res_df):
        messagebox.showinfo("Поиск", "Ничего не найдено")
        return None

    boo_window = tk.Toplevel(window)
    boo_window.geometry('1100x400+200+100')
    boo_window.title('Найденные книги')

    f = tk.Frame(boo_window)
    f.pack(fill=tk.BOTH, expand=1)
    pt = Table(f, dataframe=res_df, showtoolbar=True, showstatusbar=True)
    pt.autoResizeColumns()
    pt.show()


def search_author(author_name, window):
    """
    Поиск книги по автору. Работает методами библиоткеи pandas с DataFrame.
    Выбирает все книги в которых хотя бы Имя или Фамилия хотя бы одного автора совпадает со значением author_name.

    Parameters
    ----------
    author_name: str
        Введенное пользователем занчение автора книги, которе нужно найти
    window: Any
        Объект tk.Tk() основного окна приложения

    Returns
    -------
    None
    """
    df = load_json()
    for index, value in df['author'].items():
        find = []
        for name in value.split(', '):
            find.extend(name.split())
        if author_name not in find:
            df.drop(index, inplace=True)

    if not len(df):
        messagebox.showinfo("Поиск", "Ничего не найдено")
        return None

    boo_window = tk.Toplevel(window)
    boo_window.geometry('1100x400+200+100')
    boo_window.title('Найденные книги')

    f = tk.Frame(boo_window)
    f.pack(fill=tk.BOTH, expand=1)
    pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
    pt.autoResizeColumns()
    pt.show()
