
from unittest.mock import MagicMock
import pytest
from setup_db import db

from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    movie_1 = Movie(
        director_id=1,
        id=1,
        director=dict(id=1, name="Тейлор Шеридан"),
        genre_id=17,
        description="Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора «Ветреной реки»",
        year=2018,
        title="Йеллоустоун",
        genre=dict(id=17, name="Вестерн"),
        trailer="https://www.youtube.com/watch?v=UKei_d0cbP4",
        rating=8.6
    )

    movie_2 = Movie(
        director_id=1,
        id=1,
        director=dict(id=2, name="Квентин Тарантино"),
        genre_id=4,
        description="США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке",
        year=2015,
        title="Омерзительная восьмерка",
        genre=dict(id=4, name="Драма"),
        trailer="https://www.youtube.com/watch?v=lmB9VWm0okU",
        rating=7.8
    )

    movie_3 = Movie(
        director_id=3,
        id=3,
        director=dict(id=3, name="Владимир Вайншток"),
        genre_id=17,
        description="События происходят в конце XIX века на Диком Западе, в Америке",
        year=2018,
        title="Вооружен и очень опасен",
        genre=dict(id=17, name="Вестерн"),
        trailer="https://www.youtube.com/watch?v=UKei_d0cbP4",
        rating=8.6
    )

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie != None
        assert movie.id != None

    def test_get_all(self):
        movie = self.movie_service.get_all()
        assert len(movie) > 0

    def test_create(self):
        movie_d = {
            "director_id": 2,
            "director": {
                "id": 2,
                "name": "Квентин Тарантино"
            },
            "genre_id": 17,
            "description": "Эксцентричный охотник за головами, также известный как Дантист, промышляет отстрелом самых опасных преступников. Работенка пыльная, и без надежного помощника ему не обойтись. Но как найти такого и желательно не очень дорогого? Освобождённый им раб по имени Джанго – прекрасная кандидатура. Правда, у нового помощника свои мотивы – кое с чем надо сперва разобраться.",
            "year": 2012,
            "title": "Джанго освобожденный",
            "genre": {
                "id": 17,
                "name": "Вестерн"
            },
            "trailer": "https://www.youtube.com/watch?v=2Dty-zwcPv4",
            "rating": 8.4
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id != None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            "director_id": 2,
            "id": 2,
            "director": {
                "id": 2,
                "name": "Квентин Тарантиннно"
            },
            "genre_id": 4,
            "description": "США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке Вешатель конвоирует заключенную. По пути к ним прибиваются еще несколько путешественников. Снежная буря вынуждает компанию искать укрытие в лавке на отшибе, где уже расположилось весьма пестрое общество: генерал конфедератов, мексиканец, ковбой… И один из них - не тот, за кого себя выдает.",
            "year": 2015,
            "title": "Омерзительная восьмерка",
            "genre": {
                "id": 4,
                "name": "Драма"
            },
            "trailer": "https://www.youtube.com/watch?v=lmB9VWm0okU",
            "rating": 7.8
        }
        self.movie_service.update(movie_d)

