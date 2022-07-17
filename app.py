# app.py

from flask import Flask, request, json
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}
db = SQLAlchemy(app)

api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


"""Схема модели movie"""


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    director_id = fields.Int()


"""Схема для модели director"""


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


"""Схема для модели genre"""


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


"""Объекты схемы для модели фильмов"""

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

"""Объекты схемы для модели режиссеров"""

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

"""Объекты схемы для модели жанров"""

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

"""Эндпоинт movies для отображения всех фильмов для get запроса"""


@movie_ns.route('/')
class MovieViews(Resource):
    def get(self):
        all_movies = db.session.query(Movie)
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        if director_id is not None:
            all_movies = all_movies.filter(Movie.director_id == director_id)

        if genre_id is not None:
            all_movies = all_movies.filter(Movie.genre_id == genre_id)

        movies = all_movies.all()

        return movies_schema.dump(movies), 200

    def post(self):
        movie = movie_schema.load(request.json)
        db.session.add(Movie(**movie))
        db.session.commit()

        return 'Working', 201


"""Эндпоинт /movies/mid для отображения фильма для get запроса по его id"""


@movie_ns.route('/<int:mid>')
class MovieViews(Resource):
    def get(self, mid):
        try:
            movie = db.session.query(Movie).get(mid)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return '', 404

    def put(self, mid):
        db.session.query(Movie).filter(Movie.id == mid).update(request.json)
        db.session.commit()

    def delete(self, mid):
        db.session.query(Movie).filter(Movie.id == mid).delete()
        db.session.commit()

        return 'Working', 204


"""Эндпоинт directors для отображения всех режиссеров для get запроса"""


@director_ns.route('/')
class DirectorViews(Resource):
    def get(self):
        all_directors = db.session.query(Director).all()

        return directors_schema.dump(all_directors), 200

    def post(self):
        director = director_schema.load(request.json)
        db.session.add(Director(**director))
        db.session.commit()

        return 'Working', 201


"""Эндпоинт /directors/did для отображения режиссера для get запроса по его id"""


@director_ns.route('/<int:did>')
class DirectorViews(Resource):
    def get(self, did):
        try:
            director = db.session.query(Director).get(did)
            return director_schema.dump(director), 200
        except Exception as e:
            return '', 404

    def put(self, did):
        db.session.query(Director).filter(Director.id == did).update(request.json)
        db.session.commit()

    def delete(self, did):
        db.session.query(Director).filter(Director.id == did).delete()
        db.session.commit()

        return 'Working', 204


"""Эндпоинт genres для отображения всех фильмов для get запроса"""


@genre_ns.route('/')
class GenreViews(Resource):
    def get(self):
        all_genres = db.session.query(Genre).all()

        return genres_schema.dump(all_genres), 200

    def post(self):
        genre = genre_schema.load(request.json)
        db.session.add(Genre(**genre))
        db.session.commit()


"""Эндпоинт /genres/mid для отображения  для get запроса по его id"""


@genre_ns.route('/<int:gid>')
class GenreViews(Resource):
    def get(self, gid):
        try:
            genre = db.session.query(Genre).get(gid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return '', 404

    def put(self, gid):
        db.session.query(Genre).filter(Genre.id == gid).update(request.json)
        db.session.commit()

    def delete(self, gid):
        db.session.query(Genre).filter(Genre.id == gid).delete()
        db.session.commit()

        return 'Working', 204


if __name__ == '__main__':
    app.run(debug=True)
