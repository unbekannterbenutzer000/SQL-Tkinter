import customtkinter as cutk
from abc import ABC
import pymysql.cursors
import tkinter.messagebox as msg
import pandas as pd
import warnings
import queue

warnings.filterwarnings('ignore')

cutk.set_default_color_theme("green")


class Main(ABC):
    def connection(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='root',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.Cursor)
        return

    def connection1(self):
        self.connection1 = pymysql.connect(host='localhost',
                                           user='root',
                                           password='root',
                                           charset='utf8mb4',
                                           db=page1.BD_name.get(),
                                           cursorclass=pymysql.cursors.Cursor)
        return


class BD(Main):
    def __init__(self):
        self.sql1 = None
        self.df1 = None
        self.sql2 = None
        self.df2 = None
        return

    def createdb(self):
        Main.connection(self)
        with self.connection.cursor() as cursor:
            self.sql1 = f"CREATE DATABASE IF NOT EXISTS {page1.BD_name.get()}"
            cursor.execute(self.sql1)
            self.connection.commit()
            self.df1 = pd.read_sql("SHOW DATABASES", self.connection)  # считывание информации из базы данных

            msg.showinfo("Базы данных", str(self.df1))
            self.connection.close()
        return

    def createtb(self):
        Main.connection1(self)
        with self.connection1.cursor() as cursor:
            self.sql2 = f"CREATE TABLE IF NOT EXISTS {page1.TB_name.get()} (ID int, Стэк MEDIUMTEXT);"
            cursor.execute(self.sql2)
            self.connection1.commit()
            self.df2 = pd.read_sql("SHOW TABLES", self.connection1)  # считывание информации из базы данных
            msg.showinfo("Базы данных", str(self.df2))
            self.connection1.close()
        return

    def get_input_dbname(self):
        msg.showinfo("Уведомление", "Название БД отправлено!")
        return

    def get_input_dbtable(self):
        msg.showinfo("Уведомление", "Название таблицы отправлено!")
        return

    def delete(self):
        Main.connection1(self)
        with self.connection1.cursor() as cursor:
            self.sql1 = f"""DROP DATABASE {page1.BD_name.get()}"""
            cursor.execute(self.sql1)
            self.connection1.commit()
            self.connection1.close()
            msg.showinfo("Уведомление", "База данных удалена")
        return


class win1:
    def __init__(self):
        self.BD_name = None
        self.TB_name = None
        return

    def start(self):
        window = cutk.CTk()
        window.geometry("643x163")
        window.iconbitmap(r'scam.ico')
        window.title("Прага")

        text = cutk.CTkLabel(window, text="Введите название БД:")
        text.grid(row=0, column=0, padx=5, pady=5)
        self.BD_name = cutk.CTkEntry(window, textvariable=cutk.StringVar())
        self.BD_name.grid(row=0, column=1, pady=7, ipadx=30)
        btn_db = cutk.CTkButton(window, text="Отправить название БД", command=SQL.get_input_dbname)
        btn_db.grid(row=0, column=2, padx=10, pady=7, ipadx=36)

        # блок названия таблицы
        text1 = cutk.CTkLabel(window, text="Введите название таблицы:")
        text1.grid(row=1, column=0, pady=5, padx=10)
        self.TB_name = cutk.CTkEntry(window, textvariable=cutk.StringVar())
        self.TB_name.grid(row=1, column=1, pady=5, ipadx=30)
        btn_tb = cutk.CTkButton(window, text="Отправить название таблицы", command=SQL.get_input_dbtable)
        btn_tb.grid(row=1, column=2, pady=5, ipadx=8)

        # блок создания БД и таблицы в ней
        btn_cdb = cutk.CTkButton(window, text="Создание БД и msg", command=SQL.createdb)
        btn_cdb.grid(row=2, column=0, padx=5, pady=5, ipadx=30)
        btn_itb = cutk.CTkButton(window, text="Отправить данные в таблицу", command=page2.start)
        btn_itb.grid(row=2, column=1, pady=5, padx=5)
        btn_ctb = cutk.CTkButton(window, text="Создание таблицы в БД и msg", command=SQL.createtb)
        btn_ctb.grid(row=2, column=2, ipadx=7)

        # нижний блок
        btn_excel = cutk.CTkButton(window, text="Экспорт в Excel", command=page3.start)
        btn_excel.grid(row=3, column=0, ipadx=32, pady=5, padx=5)
        btn_del = cutk.CTkButton(window, text="Удалить БД", command=SQL.delete)
        btn_del.grid(row=3, column=1, pady=5, ipadx=44, padx=5)
        btn_q = cutk.CTkButton(window, text="Выйти из программы", command=quit, fg_color="#DB3E39",
                               hover_color="#821D1A")
        btn_q.grid(row=3, column=2, pady=5, ipadx=50, padx=5)

        window.mainloop()
        return


class win2(Main):
    def __init__(self):
        self.sql = None
        self.df = None
        return

    def start(self):
        window2 = cutk.CTk()
        window2.title("Ввод")
        window2.geometry("327x125")
        window2.iconbitmap(r'scam.ico')

        # Поле 1
        text2 = cutk.CTkLabel(window2, text="Введите ID")
        text2.grid(column=0, row=0, pady=5)
        self.string_id = cutk.CTkEntry(window2, textvariable=cutk.StringVar())
        self.string_id.grid(column=1, row=0)

        # Поле 2
        text3 = cutk.CTkLabel(window2, text="Введите стэк")
        text3.grid(column=0, row=1, pady=5, padx=5)
        self.data_input = cutk.CTkEntry(window2, textvariable=cutk.StringVar())
        self.data_input.grid(column=1, row=1)

        # Кнопка для сохранения результата
        btn_mult = cutk.CTkButton(window2, text="Сохранить", command=self.to_sql)
        btn_mult.grid(column=0, row=4, padx=10, pady=10, ipadx=0)

        # Кнопка закрытия окна
        btn_cls = cutk.CTkButton(window2, text="Закрыть окно", command=window2.destroy, fg_color="#DB3E39",
                                 hover_color="#821D1A")
        btn_cls.grid(column=1, row=4, padx=5, pady=10, ipadx=10)

        window2.mainloop()
        return

    def to_sql(self):
        stroka = page2.data_input.get()
        stek = queue.LifoQueue(maxsize=500)
        for i in stroka.split():
            stek.put(i)

        data = ''
        while not stek.empty():
            data += str(stek.get())
            data += ' '
        data = data[::-1]

        msg.showinfo('Внесенные данные', data)
        # # indexes = list(filter(lambda i: int(sps[i]) % 2 == 0, range(len(sps))))
        #
        # sps1 = ' '.join(str(sps))
        # sps2 = ' '.join(str(indexes))
        # msg.showinfo("Ответ", sps2)

        Main.connection1(self)
        with self.connection1.cursor() as cursor:
            self.sql3 = f"INSERT INTO {page1.TB_name.get()} (ID, Стэк) VALUES (%s, %s)"
            cursor.execute(self.sql3, (page2.string_id.get(), data))
            self.connection1.commit()
            self.df3 = pd.read_sql_query(f"SELECT * from {page1.TB_name.get()}", self.connection1)
            msg.showinfo("Данные из таблицы MySQL", str(self.df3))
            self.connection1.close()
        return


class win3(Main):
    def start(self):
        window3 = cutk.CTk()
        window3.title("Экспорт в Excel")
        window3.geometry("370x87")
        window3.iconbitmap(r'scam.ico')

        # Поле 1
        text7 = cutk.CTkLabel(window3, text="Введите название файла:")
        text7.grid(row=0, column=0, padx=10, pady=10)
        self.entry_widget_10 = cutk.CTkEntry(window3, placeholder_text="Excel.xlsx")
        self.entry_widget_10.grid(row=0, column=1, ipadx=10)
        # Кнопка отправки данных в таблицу
        btn_exp = cutk.CTkButton(window3, text="Экспортировать данные", command=self.save)
        btn_exp.grid(row=1, column=1, padx=5)
        # Кнопка закрытия окна
        btn15 = cutk.CTkButton(window3, text="Закрыть окно", command=window3.destroy, fg_color="#DB3E39",
                               hover_color="#821D1A")
        btn15.grid(row=1, column=0, padx=10, pady=2)

        window3.mainloop()
        return

    def save(self):
        Main.connection1(self)
        df4 = pd.read_sql_query(f"SELECT * FROM {page1.TB_name.get()}", self.connection1)
        df4.to_excel(self.entry_widget_10.get(), sheet_name='Данные из MySQL', index=False)
        # index=False значения предаются без нумерации
        return


page1 = win1()
page2 = win2()
page3 = win3()
SQL = BD()

page1.start()
