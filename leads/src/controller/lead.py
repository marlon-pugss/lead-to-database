import logging
from typing import Optional, Union

from ..schema import lead as schema
from ..db import lead as db
from ..exception import NotFoundException
from ..model.lead import Lead

logger = logging.getLogger()


def create(lead: schema.Lead) -> Optional[schema.LeadOut]:
    db_lead = db.create_lead(lead)
    if not db_lead:
        logger.warning("Failed to create lead in database")
        return None
        
    logger.info(f"Lead created in database with ID: {db_lead.id}")
    return schema.LeadOut(id=str(db_lead.id))

def get(lead_id: str) -> Lead:
    lead = db.get_lead_by_id(lead_id)
    if not lead:
        raise NotFoundException("Lead Not found")

    return lead

