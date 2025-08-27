import json
import logging
from datetime import date, datetime

from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func, event, inspect
from sqlalchemy.orm import Mapped, class_mapper, mapped_column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.attributes import get_history

from ..db import Base, BaseAudit, engine

logger = logging

ACTION_CREATE = "I"
ACTION_UPDATE = "U"
ACTION_DELETE = "D"


class BaseModel(Base):
    """Base model for all models"""
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        unique=True,
        default=lambda: str(uuid4()),
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )

    def to_dict(self):
        def convert_value(value):
            if isinstance(value, UUID):
                return str(value)
            elif isinstance(value, (date, datetime)):
                return value.isoformat()
            return value

        data = (
            lambda col: (col.key, convert_value(getattr(self, col.key))),
            class_mapper(self.__class__).columns,
        )
        return dict(data)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Desabilitado temporariamente para testes
        # event.listen(cls, "after_insert", cls.audit_insert)
        # event.listen(cls, "after_delete", cls.audit_delete)
        # event.listen(cls, "after_update", cls.audit_update)

    @staticmethod
    def audit_insert(mapper, connection, target):
        BaseModel.create_audit(target, ACTION_CREATE)

    @staticmethod
    def audit_delete(mapper, connection, target):
        BaseModel.create_audit(target, ACTION_DELETE)

    @staticmethod
    def audit_update(mapper, connection, target):
        BaseModel.create_audit(target, ACTION_UPDATE)

    @staticmethod
    def create_audit(target, action):
        try:
            audit_class = target.__class__.__name__ + "Audit"
            from . import audit

            if not hasattr(audit, audit_class):
                logger.error(f"Audit class {audit_class} not found in audit module.")
                return

            state_before = {}
            state_after = {}

            if action == ACTION_UPDATE:
                inspr = inspect(target)

            attrs = class_mapper(target.__class__).column_attrs

            for attr in attrs:
                if attr.key in ["created_at", "updated_at"]:
                    date_val = getattr(target, attr.key)
                    if isinstance(date_val, datetime):
                        setattr(target, attr.key, date_val.isoformat())

                if action == ACTION_UPDATE:
                    hist = getattr(inspr.attrs, attr.key).history
                    if hist.has_changes():
                        try:
                            state_before[attr.key] = get_history(target, attr.key)[2].pop()
                        except Exception:
                            state_before[attr.key] = f"field not retrieved {attr.key}"
                        state_after[attr.key] = getattr(target, attr.key)
                elif action == ACTION_CREATE:
                    state_after[attr.key] = getattr(target, attr.key)
                else:
                    state_before[attr.key] = getattr(target, attr.key)

            properties = {
                "state_before": json.dumps(state_before, default=str),
                "state_after": json.dumps(state_after, default=str),
                "created_at": func.now(),
                "action": action,
                "id_object": str(getattr(target, class_mapper(target.__class__).primary_key[0].key)),
            }

            audit_table = BaseAudit.metadata.tables.get(target.__tablename__ + "_audit")

            logger.info(f"Inserting audit for {target.__tablename__}: {properties}")

            with engine.connect() as audit_connection:
                transaction = audit_connection.begin()
                try:
                    audit_connection.execute(audit_table.insert().values(**properties))
                    transaction.commit()

                    inserted_row = audit_connection.execute(
                        audit_table.select().where(
                            audit_table.c.id_object == properties["id_object"]
                        )
                    ).fetchone()

                    if inserted_row:
                        logger.info(
                            "Insertion verified: row inserted with id_object "
                            f"{properties['id_object']}"
                        )
                    else:
                        logger.error(
                            "Error verifying insertion: row not found with "
                            f"id_object {properties['id_object']}"
                        )
                        raise Exception(
                            "Insertion failed, row not found after insertion"
                        )

                except SQLAlchemyError as e:
                    transaction.rollback()
                    logger.error(f"Error during insertion into audit table: {e}")
                    raise

        except Exception as e:
            logger.error(f"[base.create_audit] Error generating audit: {e}")
            raise


metadata = Base.metadata
metadata_audit = BaseAudit.metadata