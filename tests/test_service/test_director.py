
from service.director import DirectorService

from unittest.mock import MagicMock
import pytest
from setup_db import db

from dao.director import DirectorDAO
from dao.model.director import Director


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    tailor = Director(id=1, name='Тейлор Шеридан')
    kventin = Director(id=2, name='Квентин Тарантино')
    vladimir = Director(id=3, name='Владимир Вайншток')

    director_dao.get_one = MagicMock(return_value=tailor)
    director_dao.get_all = MagicMock(return_value=[tailor, kventin, vladimir])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director != None
        assert director.id != None

    def test_get_all(self):
        director = self.director_service.get_all()
        assert len(director) > 0

    def test_create(self):
        director_d = {
            "name": "Ivan",
        }
        director = self.director_service.create(director_d)
        assert director.id != None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        director_d = {
            "id": 3,
            "name": "Владимир Вайншток"
        }
        self.director_service.update(director_d)

