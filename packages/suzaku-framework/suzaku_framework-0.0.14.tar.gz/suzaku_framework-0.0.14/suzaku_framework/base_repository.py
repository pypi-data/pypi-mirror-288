# -*- encoding: utf-8 -*-

'''
Author     :Phailin
Datetime   :2023-08-01 09:00:00
E-Mail     :phailin791@hotmail.com
'''

from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session, Query
from sqlalchemy import delete, insert, update
from contextlib import AbstractContextManager
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union,Callable, Iterator, List

from suzaku_framework.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, 
        session_factory: Callable[..., AbstractContextManager[Session]],
        model: Type[ModelType]) -> None:
        self.session_factory = session_factory
        self.model = model

    def get(self, id: Any) -> Optional[ModelType]:
        # database
        with self.session_factory() as session:
            db_obj = session.query(self.model).filter(self.model.id == id, self.model.deleted==0).first()
            return db_obj

    def get_all(self) -> Iterator[ModelType]:
        # database
        with self.session_factory() as session:
            return session.query(self.model).filter_by(deleted=0).all()

    def paginate(self, queryset:Query, page: int = 1, per_page: int = 20):
        # parse per_page
        _query_offset = (page - 1) * per_page
        # items
        items = queryset.limit(per_page).offset(_query_offset).all()
        # count
        total = queryset.order_by(None).count()
        return total, items

    def create(self, obj_in: CreateSchemaType, *args, **kwargs) -> ModelType:
        # parse obj_data
        obj_in_data = jsonable_encoder(obj_in)
        # update obj_data
        obj_in_data.update(**kwargs)
        # instance
        db_obj = self.model(**obj_in_data)  # type: ignore
        # database
        with self.session_factory() as session:
            # set common value
            db_obj.created_at = datetime.now()
            db_obj.deleted = False
            # database
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def update(self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]], *args, **kwargs) -> ModelType:
        # parse obj_data
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        # update obj_data
        obj_data.update(**kwargs)
        # set business data of obj_data
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        # database 
        with self.session_factory() as session:
            # set common value
            db_obj.updated_at = datetime.now()
            # database
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def removed(self, db_obj: ModelType, *args, **kwargs) -> ModelType:
        with self.session_factory() as session:
            # set common value
            db_obj.updated_at = datetime.now()
            db_obj.deleted = True
            for field in kwargs:
                if field in jsonable_encoder(db_obj).keys():
                    setattr(db_obj, field, kwargs[field])
            # database
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def deleted(self, id: int, *args, **kwargs) -> ModelType:
        with self.session_factory() as session:
            obj = session.query(self.model).get(id)
            session.delete(obj)
            session.commit()
            return obj
        
    def batch_insert(self, db_objs: List[ModelType], *args, **kwargs):
        with self.session_factory() as session:
            for chunk in range(0, len(db_objs)+1, 1000):
                session.add_all(db_objs[chunk:chunk+1000])
                session.flush()
            session.commit()

    def batch_update(self, filter_kwargs: Dict, update_kwargs: Dict):
        with self.session_factory() as session:
            stmt = update(self.model)
            if filter_kwargs:
                stmt = stmt.where(**filter_kwargs)
            if update_kwargs:
                stmt = stmt.values(**update_kwargs)
            # sysnc
            stmt = stmt.execution_options(synchronize_session=False)
            # execute
            results =session.execute((stmt))
            # commit
            session.commit()
            # refresh
            session.refresh(results)
            # return
            return results

    def bulk_update(self, db_objs: List[ModelType], *args, **kwargs)-> List[ModelType]:
        with self.session_factory() as session:
            # update
            for chunk in range(0, len(db_objs), 1000):
                db_objs_chunk = db_objs[chunk:chunk+1000]
                session.execute(
                    update(self.model),
                    db_objs_chunk
                )
                session.flush()
            # commit
            session.commit()