
from unittest.mock import MagicMock
import pytest
from setup_db import db

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

    comedy = Genre(id=1, name='Комедия')
    family = Genre(id=2, name='Семейный')
    fantasy = Genre(id=3, name='Фэнтези')

    genre_dao.get_one = MagicMock(return_value=comedy)
    genre_dao.get_all = MagicMock(return_value=[comedy, family, fantasy])
    genre_dao.create = MagicMock(return_value=Genre(id=3))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre != None
        assert genre.id != None

    def test_get_all(self):
        genre = self.genre_service.get_all()
        assert len(genre) > 0

    def test_create(self):
        genre_d = {
            "name": "Ivan",
        }
        genre = self.genre_service.create(genre_d)
        assert genre.id != None

    def test_delete(self):
        self.genre_service.delete(1)

    def test_update(self):
        genre_d = {
            "id": 3,
            "name": "Владимир"
        }
        self.genre_service.update(genre_d)

