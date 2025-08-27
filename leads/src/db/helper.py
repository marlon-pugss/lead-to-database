from ..schema.lead import Lead as SchemaLead

from ..model import Lead


def build_lead_db(schema_lead: SchemaLead):

    additional_fields = {}
    schema_lead_json = schema_lead.model_dump()
    for i in schema_lead_json.keys():
        if not hasattr(Lead, i) and schema_lead_json.get(i) is not None:
            additional_fields[i] = schema_lead_json.get(i)

    return Lead(
        first_name=schema_lead.first_name,
        last_name=schema_lead.last_name,
        email=schema_lead.email,
        phone=schema_lead.phone,
        lead_source=schema_lead.lead_source,
        legacy=schema_lead.legacy,
        legacy_tag=schema_lead.legacy_tag,
        utm_campaign=schema_lead.utm_campaign,
        utm_source=schema_lead.utm_source,
        url_source=schema_lead.url_source,
        utm_content=schema_lead.utm_content,
        utm_medium=schema_lead.utm_medium,
        utm_term=schema_lead.utm_term,
        lead_action=schema_lead.lead_action,
        locale=schema_lead.locale,
        #opt_in=schema_lead.opt_in,
        status=schema_lead.status,
        owner_id=schema_lead.owner_id,
        additional_fields=additional_fields
    )