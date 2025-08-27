from sqlalchemy import String, Boolean, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
import enum


class Brand(str, enum.Enum):
    FLUENCY_BR = "FLUENCY_BR"
    FLUENCY_LATAM = "FLUENCY_LATAM"
    INTENSIVE = "INTENSIVE"
    B2B = "B2B"


class LeadSourceConfiguration(BaseModel):
    __tablename__ = "lead_source_configuration"

    lead_source: Mapped[str] = mapped_column(
        String,
        nullable=False,
        primary_key=True
    )

    brand: Mapped[str] = mapped_column(
        Enum(Brand),
        nullable=False
    )

    send_to_salesforce: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="true"
    )

    hold_pipeline: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="true"
    )

    percentual_to_bot: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    user: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default="admin"
    )