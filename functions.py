import sqlite3


def find_title(title):
    """
    Функция возвращает совпадение по указанной части названия (title). Если в результате работы функции получено
    несколько совпадений, то выводится запись со старшей записью release_year
    :param title: набор символов для поиска
    :return: последний выпущенный фильм по совпадению (title)
    """
    dict_netflix = []  # создание списка записей базы данных для последующего анализа
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        query_sqlite = ("""
                        SELECT title, country, release_year, listed_in, description
                        FROM netflix
                        WHERE type = 'Movie'
        """)
        cursor.execute(query_sqlite)
        extract = cursor.fetchall()
        for row in extract:  # перебор для пополнения списка python
            dict_netflix.append(row)

    list_of_coincidence = [row for row in dict_netflix if title.lower() in row[0].lower()]  # перебор всех записей из
    # списка записей БД на совпадение по переданному значению и запись их в список

    if list_of_coincidence:  # алгоритм выполняется в случае наличия в списке совпадений хотя бы одной записи

        for i, row in enumerate(list_of_coincidence, start=1):  # перебор списка совпадений по значению release_year
            # для определения записи с последней актуальной датой выпуска
            if i == 1:
                found_movie = row
            elif i > 1 and row[2] > found_movie[2]:
                found_movie = row

        result = {  # создание читабельного отображения
            "title": found_movie[0],
            "country": found_movie[1],
            "release_year": found_movie[2],
            "genre": found_movie[3],
            "description": found_movie[4]
        }

        symbol = '\n'  # удаление знака переноса строки из description
        if symbol in result['description']:
            result['description'] = result['description'].replace(symbol, '')

        return result
    return 'Не найдено'  # возвращается в случае отсутствия совпадений


def find_movies_of_certain_years(start, finish):
    """
    Функция возвращает список фильмов за указанный диапазон (start, finish)
    :param start: начало диапазона (значение должно быть больше finish).
    :param finish: окончание диапазона (значение должно быть меньше start)
    :return: список фильмов за указанный диапазон (список ограничен 100 записями)
    """
    dict_netflix = []  # создание списка записей базы данных для последующего анализа
    with sqlite3.connect('netflix.db') as connection:  # подключение к БД
        cursor = connection.cursor()  # вызов курсора для обработки запроса
        query_sqlite = ("""
                            SELECT title, release_year
                            FROM netflix
                            WHERE type = 'Movie'
            """)
        cursor.execute(query_sqlite)  # выполнение запроса
        extract = cursor.fetchall()  # извлечение результата
        for row in extract:  # пополнение списка словарей для последующего анализа
            dict_intermediate = {'title': row[0], 'release_year': row[1]}
            dict_netflix.append(dict_intermediate)

    list_of_films = sorted(dict_netflix, key=lambda x: x['release_year'], reverse=True)  # создание и сортировка
    # списка фильмов

    try:  # запуск цикла с корректными данными
        if start >= finish:
            result_list = []  # создание финального списка для вывода значений по указанному диапазону "start & finish"
            for row in list_of_films:
                if int(finish) <= row['release_year'] <= int(start) and len(result_list) != 100:
                    result_list.append(row)

            return result_list
        else:
            return "Проверьте что start больше finish"
    except:
        return "Убедитесь, что адрес указан верно: должны быть указаны значения start и finish; значения start " \
               "должно быть больше, либо равно значению finsih. Пример: " \
               "localhost:5000/movie/year?start=2015&finish=2015"


def sort_by_rating(rating):
    """
    Функция для поиска списков по заданному рейтингу.
    :param rating: передаёт значение нужного рейтинга.
    :return: возвращает список совпадений по искомому рейтингу
    """
    with sqlite3.connect('netflix.db') as connection:  # подключение к БД
        cursor = connection.cursor()  # вызов курсора для обработки запроса
        query_sqlite = ("""
                            SELECT title, rating, description
                            FROM netflix
                            WHERE rating = 'G' 
                            OR rating = 'PG'
                            OR rating = 'PG-13'
                            OR rating = 'R'
                            OR rating = 'NC-17'
                            GROUP BY rating, title
            """)
        cursor.execute(query_sqlite)  # выполнение запроса
        extract = cursor.fetchall()  # извлечение результата

    dict_netflix = [{
        "title": row[0],
        "rating": row[1],
        "description": row[2]
    } for row in extract]  # создание списка записей базы данных для последующего анализа

    result_list = [row for row in dict_netflix if rating.lower() == row["rating"].lower()]  # создание списка
    # результатов проверки на совпадение

    if result_list:
        symbol = '\n'  # удаление знака переноса строки из description
        for row in result_list:
            if symbol in row['description']:
                row['description'] = row['description'].replace(symbol, '')

        return result_list
    else:  # вывод в случае отсутствия совпадений
        return {'Условие': 'Проверьте правильность условия',
                'Пример': 'http://localhost:5000/movie/rating?rating=G',
                'Возможнные значения переменной rating': ["G — нет возрастных ограничений", "PG — желательно " 
                "присутствие родителей', 'PG-13 — для детей от 13 лет в присутствии родителей", 'R — дети до 16 лет '
                'допускаются на сеанс только в присутствии родителей', 'NC-17 — дети до 17 лет не допускаются']}


def ten_last_new_movie(genre):
    """
    Функция для поиска 10 последних (по дате выхода) фильмов по жанру.
    :param genre: передаёт жанр.
    :return: возвращает список из 10 совпадений.
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        query_sqlite = ("""
                            SELECT title, rating, listed_in, description, release_year
                            FROM netflix
                            ORDER BY release_year DESC  
            """)
        cursor.execute(query_sqlite)
        extract = cursor.fetchall()
    dict_netflix = [{  # формируем список словарей для анализа
        "title": row[0],
        "rating": row[1],
        "genre": row[2],
        "description": row[3],
        "release_year": row[4]
    } for row in extract]
    result_list = []  # создаём пустой словарь для добавления в него совпадений
    for row in dict_netflix:
        if genre.lower() in row['genre'].lower() and len(result_list) != 10:
            result_list.append(row)
    if result_list:
        symbol = '\n'  # удаление знака переноса строки из description
        for row in result_list:
            if symbol in row['description']:
                row['description'] = row['description'].replace(symbol, '')
        return result_list
    else:
        return 'Совпадений не найдено'


def played_with_actors(actor1, actor2):
    """
    Функция выполняет задачу поиска тех актёров, которые указаны рядом с actor1 и actor2 два и более раз.
    :param actor1: первый актёр.
    :param actor2: второй актёр.
    :return: список актёров.
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        query_sqlite = ("""
                        SELECT "cast"
                        FROM netflix
                        WHERE netflix.cast != ''
            """)
        cursor.execute(query_sqlite)
        extract = cursor.fetchall()
        all_actors = [row[0] for row in extract]  # формируем список актёров из полученных кортежей

        other_actors = set()  # создаём множество, куда будут добавлены актёры которые появляются в фильмах вместе с
        # переданными в качестве аргументов актёрами
        result_list = set()  # финальное множество

        try:
            for row in all_actors:
                if actor1 in row and actor2 in row:
                    actors = row.split(', ')  # переводим строку в список для точечной проверки по актёрам
                    for actor in actors:
                        if actor in other_actors and actor != actor1 and actor != actor2:  # если актёр уже значится в
                            # промежуточном множестве, то добавляем его в результирующее множество
                            result_list.add(actor)
                        else:  # если актёр встречается впервые, добавляем его в промежуточное множество
                            other_actors.add(actor)
            result_list = list(result_list)  # переводим множество в список для вывода
            if result_list:
                return result_list
            else:
                return "Совпадений не найдено"
        except:
            return "Неверный запрос"


def query_data(q_type, q_release, q_genre):
    """
    Функция для отображения списка записей по совпадению вхождения переданных переменных.
    :param q_type: тип
    :param q_release: дата выхода
    :param q_genre: жанр
    :return: список словарей совпадений
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        query_sqlite = ("SELECT title, type, release_year, listed_in, description "
                        "FROM netflix "
                        f"WHERE type = '{q_type}' "
                        f"AND release_year = '{q_release}' "
                        f"AND listed_in LIKE '%{q_genre}%'"
                        )
        cursor.execute(query_sqlite)
        extract = cursor.fetchall()
    dict_netflix = [{
        "title": row[0],
        "type": row[1],
        "release_year": row[2],
        "listed_in": row[3],
        "description": row[4],
    } for row in extract]

    return dict_netflix
