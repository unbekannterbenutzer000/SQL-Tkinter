import tkinter as tk
from abc import ABC
import pymysql.cursors
import tkinter.messagebox as msg
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


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
                                           db=page1.entry_widget_1.get(),
                                           cursorclass=pymysql.cursors.Cursor)
        return


# главное окно проги, ввод и создание БД
class win1():
    def start(self):
        # создание окошка
        window1 = tk.Tk()
        window1.title("Прага")
        window1.geometry("610x145")

        # блок названия БД
        text = tk.Label(window1, text="Введите название БД:")
        text.grid(row=0, column=0, pady=5)
        self.entry_widget_1 = tk.Entry(window1, textvariable=tk.StringVar())
        self.entry_widget_1.grid(row=0, column=1, pady=5, ipadx=20)
        btn_db = tk.Button(window1, text="Отправить название БД", command=SQL.get_input_dbname)
        btn_db.grid(row=0, column=2, pady=5, ipadx=43)

        # блок названия таблицы
        text1 = tk.Label(window1, text="Введите название таблицы:")
        text1.grid(row=1, column=0, pady=5)
        self.entry_widget_2 = tk.Entry(window1, textvariable=tk.StringVar())
        self.entry_widget_2.grid(row=1, column=1, pady=5, ipadx=20)
        btn_tb = tk.Button(window1, text="Отправить название таблицы в БД", command=SQL.get_input_dbtable)
        btn_tb.grid(row=1, column=2, pady=5, ipadx=13)

        # блок создания БД и таблицы в ней
        btn_cdb = tk.Button(window1, text="Создание БД и вывод в окне", command=SQL.createdb)
        btn_cdb.grid(row=2, column=1, padx=5, pady=5)
        btn_ctb = tk.Button(window1, text="Создание таблицы в БД и вывод в окне", command=SQL.createtb)
        btn_ctb.grid(row=2, column=2)

        # нижний блок
        btn_itb = tk.Button(window1, text="Отправить данные в таблицу", command=page2.start)
        btn_itb.grid(row=3, column=0, pady=5, padx=10)
        btn_exc = tk.Button(window1, text="Экспорт в Excel", command=page3.start)
        btn_exc.grid(row=3, column=1, ipadx=36, pady=5)
        btn_q = tk.Button(window1, text="Выйти из программы", command=quit)
        btn_q.grid(row=3, column=2, pady=5, ipadx=48, padx=5)

        window1.mainloop()


# окно с вводом данных в БД
class win2(Main):
    def __init__(self):
        self.sql = None
        self.df = None
        return

    def start(self):
        window2 = tk.Tk()
        window2.title("Ввод")
        window2.geometry("320x120")

        # Поле 1
        text2 = tk.Label(window2, text="Введите ID")
        text2.grid(column=0, row=0, pady=10)
        self.entry_widget_3 = tk.Entry(window2, textvariable=tk.StringVar())
        self.entry_widget_3.grid(column=1, row=0)
        # Поле 2
        text3 = tk.Label(window2, text="Введите Исходный список")
        text3.grid(column=0, row=1, pady=5, padx=10)
        self.entry_widget_4 = tk.Entry(window2, textvariable=tk.StringVar())
        self.entry_widget_4.grid(column=1, row=1)
        # Кнопка для сохранения результата
        btn_mult = tk.Button(window2, text="Сохранить", command=self.to_sql)
        btn_mult.grid(column=0, row=4, padx=15, pady=10)
        # Кнопка закрытия окна
        btn_cls = tk.Button(window2, text="Закрыть окно", command=window2.destroy)
        btn_cls.grid(column=1, row=4, padx=10, pady=10, ipadx=20)
        return

    def to_sql(self):
        sps = list(map(int, page2.entry_widget_4.get().split()))
        pos, neg = [], []
        for i in sps:
            if i >= 0:
                pos.append(i)
            else:
                neg.append(i)
        sps1 = ' '.join(str(sps))
        sps2 = ' '.join(str(pos))
        sps3 = ' '.join(str(neg))
        msg.showinfo("Ответ", sps2 + '\n' + sps3)
        Main.connection1(self)
        with self.connection1.cursor() as cursor:
            self.sql3 = f"INSERT INTO {page1.entry_widget_2.get()} (ID, Исходник, Положительные, Отрицательные) VALUES (%s, %s, %s, %s)"
            cursor.execute(self.sql3, (page2.entry_widget_3.get(), sps1, sps2, sps3))
            self.connection1.commit()
            self.df3 = pd.read_sql_query(f"SELECT * from {page1.entry_widget_2.get()}", self.connection1)
            msg.showinfo("Данные из таблицы MySQL", str(self.df3))
            self.connection1.close()
        return


# окно создания эксель файла
class win3(Main):
    def start(self):
        window3 = tk.Tk()
        window3.title("Экспорт в Excel")
        window3.resizable()
        canvas1 = tk.Canvas(window3)
        canvas1.pack()
        # Поле 1
        text7 = tk.Label(canvas1, text="Введите название файла Excel.xlsx")
        text7.pack(expand=True, padx=10, pady=10)
        self.entry_widget_10 = tk.Entry(canvas1, textvariable=tk.StringVar())
        self.entry_widget_10.pack()
        # Кнопка отправки данных в таблицу
        btn_exp = tk.Button(canvas1, text="Экспортировать данные в Excel", command=self.save)
        btn_exp.pack(padx=50, pady=2)
        # Кнопка закрытия окна
        btn15 = tk.Button(canvas1, text="Закрыть окно", command=window3.destroy)
        btn15.pack(padx=50, pady=2)
        return

    def save(self):
        Main.connection1(self)
        df4 = pd.read_sql_query(f"SELECT * FROM {page1.entry_widget_2.get()}", self.connection1)
        df4.to_excel(self.entry_widget_10.get(), sheet_name='Данные из MySQL', index=False)
        # index=False значения предаются без нумерации
        return


# создание БД и таблицы
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
            self.sql1 = f"CREATE DATABASE IF NOT EXISTS {page1.entry_widget_1.get()}"
            cursor.execute(self.sql1)
            self.connection.commit()
            self.df1 = pd.read_sql("SHOW DATABASES", self.connection)  # считывание информации из базы данных
            msg.showinfo("Базы данных", str(self.df1))
            self.connection.close()
        return

    def get_input_dbname(self):
        msg.showinfo("Уведомление", "Название БД передано!")
        return

    def createtb(self):
        Main.connection1(self)
        with self.connection1.cursor() as cursor:
            self.sql2 = f"CREATE TABLE IF NOT EXISTS {page1.entry_widget_2.get()} (ID int, Исходник varchar(2000), Положительные varchar(2000), Отрицательные varchar(2000));"
            cursor.execute(self.sql2)
            self.connection1.commit()
            self.df2 = pd.read_sql("SHOW TABLES", self.connection1)  # считывание информации из базы данных
            msg.showinfo("Базы данных", str(self.df2))
            self.connection1.close()
        return

    def get_input_dbtable(self):
        msg.showinfo("Уведомление", "Название таблицы отправлено!")
        return


page1 = win1()
page2 = win2()
page3 = win3()
SQL = BD()

page1.start()
