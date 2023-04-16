import pandas as pd
import psycopg2
from psycopg2 import Error

db1 = pd.read_excel('ФПТИ_Aрхив_2022_весна.xlsx','1 курс')
db2 = pd.read_excel('ФПТИ_Aрхив_2022_весна.xlsx','2 курс')
db3 = pd.read_excel('ФПТИ_Aрхив_2022_весна.xlsx','3 курс')
db4 = pd.read_excel('ФПТИ_Aрхив_2022_весна.xlsx','4 курс')
dbm1 = pd.read_excel('ФПТИ_Aрхив_2022_весна.xlsx','1 маг')
dbm2 = pd.read_excel('ФПТИ_Aрхив_2022_весна.xlsx','2 маг')
db_profcoin = pd.read_excel('Просмотр Профкоинов.xlsx','ФПТИ',skiprows =2)
db1=db1.append(db2)
db1=db1.append(db3)
db1=db1.append(db4)
db1=db1.append(dbm1)
db1=db1.append(dbm2)
db1['ФИО'] = db1['Фамилия']+' '+db1['Имя']
db1 = pd.merge(db1, db_profcoin, on="ФИО", how="left")
db1['Кол-во профкоинов'] = db1['Кол-во профкоинов'].fillna(0)
db1['Кол-во профкоинов'] = db1['Кол-во профкоинов'].astype('Int64')
db1 = db1.reset_index(drop=True)
print(db1)
try:
    connection = psycopg2.connect(
                            user='postgres',
                            password = '1002amor',
                            host = 'localhost',
                            port = "5432",
                            database = "telegram")

    cursor = connection.cursor()
    for i in range(len(db1)):
        cursor.execute("INSERT INTO student VALUES({},'{}','{}','{}',{},'{}');".format(db1['№ профбилета'][i],
                                                                                       db1['Имя'][i],
                                                                                       db1['Фамилия'][i],
                                                                                       db1['Отчество'][i],
                                                                                       db1['Кол-во профкоинов'][i],
                                                                                       db1['Группа'][i]))
    connection.commit()
except(Exception, Error) as error:
    print(error)
    print('Ошибка при работе с PostgreSQL')
finally:
    cursor.close()
    connection.close()
    print("Соединение с PostgreSQL закрыто")


