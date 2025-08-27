from enum import Enum
from typing import Type, Union, Optional
from sqlalchemy import or_, func, text
from .. import db, model


def create(model: model.BaseModel) -> model.BaseModel:
    with db.session() as s:
        s.add(model)
        s.commit()
        return model


def execute(query: str) -> list:
    with db.session() as s:
        return s.execute(query).fetchall()

      
def filter(cls: Type[model.BaseModel], query_filter=None, or_clause=False) -> list:
    with db.session() as s:
        query = s.query(cls)

        if query_filter:
            if or_clause:
                query = query.filter(or_(*query_filter))
            else:
                query = query.filter(*query_filter)

        return query.all()


def filter_group_by(group_by, query_filter=None, or_clause=False, ):
    with db.session() as s:
        query = s.query(group_by, func.count().label("total_count"))
        if query_filter:
            if or_clause:
                query = query.filter(or_(*query_filter))
            else:
                query = query.filter(*query_filter)
        return query.group_by(group_by).all()


def get(
    field,
    value,
    cls: Type[model.BaseModel],
) -> Optional[model.BaseModel]:
    with db.session() as s:
        return s.query(cls).filter_by(**{field: value}).first()


def update(
    model: model.BaseModel,
    new_model: model.BaseModel,
) -> model.BaseModel:
    with db.session() as s:
        merged_model = s.merge(model)
        for attr, value in new_model.__dict__.items():
            if (
                attr != "id"
                and hasattr(merged_model, attr)
                and getattr(merged_model, attr) != value
            ):
                if isinstance(value, Enum):
                    value = value.value
                setattr(merged_model, attr, value)
        s.commit()
        return merged_model


def update_model(
    new_model: model.BaseModel,
) -> model.BaseModel:
    with db.session() as s:
        merged_model = s.merge(new_model)
        s.commit()
        return merged_model


def execute(query: str) -> list:
    with db.session() as s:

        return s.execute(text(query)).fetchall()


def schema_to_model(
    obj,
    cls: Type[model.BaseModel],
):
    model = cls()

    for field in obj.__dict__:
        if hasattr(model, field):
            if hasattr(type(obj.__dict__[field]), "dict"):
                setattr(model, field, obj.__dict__[field].__dict__)
            else:
                setattr(model, field, obj.__dict__[field])

    return model