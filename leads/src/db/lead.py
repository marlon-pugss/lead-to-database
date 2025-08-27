from typing import Optional, cast

from .base import create, get
from .helper import build_lead_db
from ..model.lead import Lead
from ..schema.lead import Lead as LeadSchema

import logging
logger = logging.getLogger()


def create_lead(lead: LeadSchema) -> Lead:
    lead_model = build_lead_db(lead)
    return cast(Lead, create(lead_model))


def get_lead_by_id(lead_id: str) -> Optional[Lead]:
    return cast(Optional[Lead], get("id", lead_id, Lead))
