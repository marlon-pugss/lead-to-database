from ...model import Lead
from ...schema.lead import LeadEvent


def build_lead_out(lead: Lead) -> LeadEvent:
    return LeadEvent(
        id=lead.id,
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        phone=lead.phone,
        status=lead.status,
        lead_source=lead.lead_source,
        utm_campaign=lead.utm_campaign,
        url_source=lead.url_source,
        utm_source=lead.utm_source,
        utm_content=lead.utm_content,
        utm_medium=lead.utm_medium,
        utm_term=lead.utm_term,
        status_reason=lead.status_reason,
        owner_id=lead.owner_id,
        brand=lead.brand,
        journey=lead.journey,
        journey_stage=lead.journey_stage,
        journey_stage_reason=lead.journey_stage_reason,
        created_at=lead.created_at,
        updated_at=lead.updated_at
    )