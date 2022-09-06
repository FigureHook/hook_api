from typing import Generic, TypeVar

from app import crud
from app.crud.base import CRUDBase
from app.models import Paintwork, Sculptor
from app.models.worker import Worker
from app.schemas.worker import WorkerCreate, WorkerUpdate
from app.tests.utils.faker import faker
from app.tests.utils.worker import (create_random_paintwork,
                                    create_random_sculptor)
from sqlalchemy.orm import Session

Worker_T = TypeVar('Worker_T', bound=Worker)


class WorkerTestCase(Generic[Worker_T]):
    crud_module: CRUDBase[Worker_T, WorkerCreate, WorkerUpdate]

    @classmethod
    def generate_worker(cls, db: Session) -> Worker_T:
        raise NotImplementedError

    def test_create(self, db: Session):
        obj_in = WorkerCreate(name=faker.name())
        db_obj = self.crud_module.create(db=db, obj_in=obj_in)
        assert db_obj.name == obj_in.name

    def test_get(self, db: Session):
        db_obj = self.generate_worker(db)
        fetched_db_obj = self.crud_module.get(db=db, id=db_obj.id)

        assert fetched_db_obj == db_obj

    def test_update_category(self, db: Session):
        db_obj = self.generate_worker(db)
        update_obj = WorkerUpdate(name=faker.name())
        updated_db_obj = self.crud_module.update(
            db=db, db_obj=db_obj, obj_in=update_obj)

        assert update_obj.name == updated_db_obj.name

    def test_delete_category(self, db: Session):
        db_obj = self.generate_worker(db)
        deleted_worker = self.crud_module.remove(db=db, id=db_obj.id)
        fetched_worker = self.crud_module.get(db=db, id=db_obj.id)

        assert not fetched_worker
        if deleted_worker:
            assert deleted_worker.name == db_obj.name


class TestPaintwork(WorkerTestCase[Paintwork]):
    crud_module = crud.paintwork

    @classmethod
    def generate_worker(cls, db: Session):
        return create_random_paintwork(db)


class TestSculptor(WorkerTestCase[Sculptor]):
    crud_module = crud.sculptor

    @classmethod
    def generate_worker(cls, db: Session):
        return create_random_sculptor(db)
