from flask import Flask, request, jsonify
from functions import find_title, find_movies_of_certain_years, sort_by_rating, ten_last_new_movie, played_with_actors,\
    query_data

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False


@app.route('/movie/title')
# вьюшка для поиска фильма по названию (или части названия)
# пример: http://localhost:5000/movie/title?title=13th
def search_movie_name():
    title = request.args.get('title')
    return jsonify(find_title(title))


@app.route('/movie/year')
# вьюшка для поиска фильмов по году выпуска
# пример: http://localhost:5000/movie/year?start=2015&finish=2015
# вывод ограничен 100 значениями
def search_movies_years():
    start = request.args.get('start')
    finish = request.args.get('finish')
    return jsonify(find_movies_of_certain_years(start, finish))


@app.route('/movie/rating')
# вьюшка для поиска фильма по рейтингу
# пример: http://localhost:5000/movie/rating?rating=G
def group_movies_by_rating():
    rating = request.args.get('rating')
    return jsonify(sort_by_rating(rating))


@app.route('/movie/genre')
# вьюшка для поиска фильма по жанру
# пример: http://localhost:5000/movie/genre?genre=drama
def new_movies():
    genre = request.args.get('genre')
    return jsonify(ten_last_new_movie(genre))


@app.route('/movie/recurring_actors')
# вьюшка для поиска актёров которые появляются в фильме два и более раз с актёрами 1 и 2
# пример: http://localhost:5000/movie/recurring_actors?actor1=Jack%20Black&actor2=Dustin%20Hoffman
def recurring_actors():
    actor1 = request.args.get('actor1')
    actor2 = request.args.get('actor2')
    return jsonify(played_with_actors(actor1, actor2))


@app.route('/movie/query')
# вьюшка для поиска фильмов с указанием type, release, genre.
# пример: http://localhost:5000/movie/query?type=&release=2002&genre=t
# либо: http://localhost:5000/movie/query
def query_database():
    q_type = request.args.get('type')
    q_release = request.args.get('release')
    q_genre = request.args.get('genre')
    if q_type is None or q_type == '':
        q_type = 'Movie'
    if q_release is None or q_release == '':
        q_release = '2002'
    if q_genre is None or q_genre == '':
        q_genre = ''
    return jsonify(query_data(q_type, q_release, q_genre))


if __name__ == "__main__":
    app.run(debug=True)
    