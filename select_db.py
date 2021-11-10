from pprint import pprint
import sqlalchemy
import os


def connection_database():
    db = {
        'drivers': 'postgresql',
        'host': 'localhost',
        'port': '5432',
        'username': 'py44',
        'password': 'py44',
        'database': 'py44'
    }
    connection_string = f'{db.get("drivers")}://{db.get("username")}:{db.get("password")}@{db.get("host")}:{db.get("port")}/{db.get("database")}'
    engine = sqlalchemy.create_engine(connection_string)
    connection = engine.connect()
    print("Connection to PostgreSQL is successful")
    return connection


# 1. количество исполнителей в каждом жанре
def task1(connection):
    query_result = connection.execute(f"""SELECT g.genre_name, count(*) as quantity
                                        FROM songs2.genre g
                                        JOIN songs2.rsSingerGenre r on r.genre_id = g.id 
                                        JOIN songs2.singer s on s.id = r.singer_id
                                        GROUP BY g.genre_name
                                        ORDER BY quantity DESC, g.genre_name ASC;""").fetchall()
    return query_result


# 2. количество треков, вошедших в альбомы 2019-2020 годов;
def task2(connection):
    query_result = connection.execute(f"""SELECT a.album_name, count(*)
                                        FROM songs2.tracks t 
                                        JOIN songs2.albums a on a.id = t.album_id 
                                        WHERE a.year_release in (2019, 2020)
                                        GROUP BY a.album_name;""").fetchall()
    return query_result


# 3. средняя продолжительность треков по каждому альбому
def task3(connection):
    query_result = connection.execute(f"""SELECT a.album_name, avg(t.duration) 
                                        FROM songs2.tracks t 
                                        JOIN songs2.albums a on a.id = t.album_id 
                                        GROUP BY a.album_name
                                        ORDER BY a.album_name;""").fetchall()
    return query_result


# 4. все исполнители, которые не выпустили альбомы в 2020 году
def task4(connection):
    query_result = connection.execute(f"""SELECT s.singer_name FROM songs2.singer s WHERE  s.id not in (
                                        SELECT s2.id
                                        FROM songs2.singer s2
                                        JOIN  songs2.rssingeralbum r on s2.id = r.singer_id
                                        JOIN songs2.albums a on a.id = r.album_id
                                        WHERE  a.year_release = 2020);""").fetchall()
    return query_result


# 5. названия сборников, в которых присутствует конкретный исполнитель (выберите сами)
def task5(connection, singer_name):
    query_result = connection.execute(f"""SELECT distinct c.collection_name
                                        FROM songs2.collections c
                                        JOIN songs2.rscollectiontrack r on r.collection_id = c.id
                                        JOIN songs2.tracks t on t.id = r.track_id
                                        JOIN songs2.albums a on a.id = t.album_id
                                        JOIN songs2.rssingeralbum r2 on r2.album_id = a.id
                                        JOIN songs2.singer s on s.id = r2.singer_id
                                        WHERE s.singer_name = {singer_name}
                                        ORDER BY c.collection_name;""").fetchall()
    return query_result


# # 6. название альбомов, в которых присутствуют исполнители более 1 жанра
def task6(connection):
    query_result = connection.execute(f"""SELECT a.album_name as album_name 
                                        FROM songs2.albums a 
                                        JOIN songs2.rssingeralbum r on r.album_id = a.id 
                                        JOIN songs2.singer s on s.id = r.singer_id 
                                        JOIN songs2.rssingergenre r2 on r2.singer_id = s.id 
                                        JOIN songs2.genre g on g.id = r2.genre_id 
                                        GROUP BY album_name 
                                        HAVING count(*) > 1
                                        ORDER BY album_name ;""").fetchall()
    return query_result


# # 7. наименование треков, которые не входят в сборники
def task7(connection):
    query_result = connection.execute(f"""SELECT t.track_name 
                                        FROM songs2.tracks t
                                        LEFT JOIN songs2.rscollectiontrack r on t.id = r.track_id
                                        WHERE r.track_id is null
                                        ORDER BY t.track_name ;""").fetchall()
    return query_result


# # 8. исполнителя(-ей), написавшего самый короткий по продолжительности трек
# # (теоретически таких треков может быть несколько)
def task8(connection):
    query_result = connection.execute(f"""SELECT s.singer_name 
                                        FROM songs2.singer s 
                                        JOIN songs2.rssingeralbum r on r.singer_id = s.id 
                                        JOIN songs2.albums a on a.id = r.album_id 
                                        JOIN songs2.tracks t on t.album_id = a.id 
                                        WHERE t.duration = (SELECT min(t.duration) FROM songs2.tracks t )
                                        ORDER BY s.singer_name ;""").fetchall()
    return query_result


# # 9. название альбомов, содержащих наименьшее количество треков
def task9(connection):
    query_result = connection.execute(f"""SELECT a.album_name
                                        FROM songs2.albums a 
                                        JOIN songs2.tracks t on t.album_id = a.id 
                                        GROUP BY a.album_name
                                        HAVING count(*) = (SELECT count(*) as quantity
                                                            FROM songs2.albums a 
                                                            JOIN songs2.tracks t on t.album_id = a.id 
                                                            GROUP BY a.album_name 
                                                            ORDER BY quantity
                                                            LIMIT 1
                                                            )
                                        ORDER BY a.album_name;""").fetchall()
    return query_result


db_connect = connection_database()

MAIN_MENU = """ 
    1 - задача 1
    2 - задача 2
    3 - задача 3
    4 - задача 4
    5 - задача 5
    6 - задача 6
    7 - задача 7
    8 - задача 8
    9 - задача 9
    0 - выход из программы
"""

result_query = db_connect.execute("""SELECT singer_name
                                        FROM songs2.singer;""").fetchall()
list_singer = []
for elem in result_query:
    list_singer.append(elem[0])
sorted(list_singer)
MENU_LIST_SINGER = ""
for item, value in enumerate(list_singer):
    MENU_LIST_SINGER += f"{item} - {value}\n"
dict_singer = {}
dict_singer.update(enumerate(list_singer))

print(dict_singer)
print(dict_singer.get('5'))

while True:
    print(f"{MAIN_MENU}")
    choice = input("Введите номер задачи: ")
    if choice == '1':
        print(task1(db_connect))
    elif choice == '2':
        print(task2(db_connect))
    elif choice == '3':
        print(task3(db_connect))
    elif choice == '4':
        print(task4(db_connect))
    elif choice == '5':
        print(f"{MENU_LIST_SINGER}")
        singer_choice = input("Выберите исполнителя: ")
        try:
            singer_choice = int(singer_choice)
            if singer_choice in dict_singer.keys():
                print(task5(db_connect, f"'{dict_singer.get(singer_choice)}'"))
            else:
                print("Такого исполнителя нет в базе!!!\n")
        except ValueError:
            print("Не верно выбран пункт!!!\n")
    elif choice == '6':
        print(task6(db_connect))
    elif choice == '7':
        print(task7(db_connect))
    elif choice == '8':
        print(task8(db_connect))
    elif choice == '9':
        print(task9(db_connect))
    elif choice == '0':
        print("Программа завершает свою работу !!!")
        break
    else:
        print("Такого пункта меню нет. Выберите правильный")
        os.system('pause')
        os.system('cls||clear')

