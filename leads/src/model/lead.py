from sqlalchemy import String, Boolean, Enum, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseModel
from ..schema.lead import Brand, LeadStatus, Journey, JourneyStage
from typing import Any, List


class Lead(BaseModel):
    __tablename__ = "leads"

    # Salesforce ID
    external_id: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    first_name: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    last_name: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    lead_source: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    legacy: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    legacy_tag: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    utm_campaign: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    url_source: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    utm_source: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    utm_content: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    utm_medium: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    utm_term: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    lead_action: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    locale: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    opt_in: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        Enum(LeadStatus),
        nullable=False,
        server_default=LeadStatus.CREATED
    )

    status_reason: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    owner_id: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    brand: Mapped[str] = mapped_column(
        Enum(Brand),
        nullable=True
    )

    journey: Mapped[str] = mapped_column(
        Enum(Journey),
        nullable=True
    )

    journey_stage: Mapped[str] = mapped_column(
        Enum(JourneyStage),
        nullable=True
    )

    journey_stage_reason: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    additional_fields: Mapped[List[dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
    )

    __table_args__ = (
        Index('idx_created_at_status', 'status', 'created_at'),
    )