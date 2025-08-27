from datetime import datetime
import unicodedata

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union
import enum


def strip_accents(txt: str) -> str:
    return (
        unicodedata.normalize("NFKD", txt)
        .encode("ascii", "ignore")
        .decode("ascii")
    )


class Lead(BaseModel):
    id: Optional[str] = Field(default=None)
    external_id: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None, alias="FirstName")
    last_name: str = Field(alias="LastName")
    email: str = Field(alias="Email")
    phone: str = Field(alias="Phone")
    lead_source: str = Field(alias="LeadSource")
    record_type: Optional[str] = Field(default="0128b000000pa26AAA", alias="RecordTypeId")
    company: Optional[str] = Field(default=None, alias="Company")
    legacy: Optional[str] = Field(default=None, alias="legacy__c")
    legacy_tag: Optional[str] = Field(default=None, alias="legacyTag__c")
    utm_campaign: Optional[str] = Field(default=None, alias="utmCampaign__c")
    url_source: Optional[str] = Field(default=None, alias="urlSource__c")
    utm_source: Optional[str] = Field(default=None, alias="utmSource__c")
    utm_content: Optional[str] = Field(default=None, alias="utmContent__c")
    utm_medium: Optional[str] = Field(default=None, alias="utmMedium__c")
    utm_term: Optional[str] = Field(default=None, alias="utmTerm__c")
    lead_action: Optional[str] = Field(default=None, alias="leadAction__c")
    locale: Optional[str] = Field(default=None, alias="Locale__c")
    opt_in: Optional[bool] = Field(default=False, alias="OptIn__c")
    status: Optional[str] = Field(default=None, alias="Status__c")
    owner_id: Optional[str] = Field(default=None, alias="OwnerId")

    @field_validator("email", mode="before")
    def email_normalize(cls, v: str) -> str:
        return strip_accents(v).strip().lower()

    @field_validator("lead_source")
    def convert_to_upper(cls, value):
        return value.upper()

    model_config = {
        "populate_by_name": True
    }


class LeadGroupedBySource(BaseModel):
    owner_id: Optional[str] = None
    total_count: int


class LeadUpdate(BaseModel):
    id: str
    journey_stage: Optional[str] = None
    owner_id: Optional[str] = None


class LeadOut(BaseModel):
    id: str


class LeadEvent(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    lead_source: str
    status: str
    utm_campaign: Optional[str] = None
    url_source: Optional[str] = None
    utm_source: Optional[str] = None
    utm_content: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_term: Optional[str] = None
    status_reason: Optional[str] = None
    owner_id: Optional[str] = None
    brand: Optional[str] = None
    journey: Optional[str] = None
    journey_stage: Optional[str] = None
    journey_stage_reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class LeadOutError(BaseModel):
    status_code: int
    detail: Union[dict, list, str]


class Brand(str, enum.Enum):
    FLUENCY_BR = "FLUENCY_BR"
    FLUENCY_LATAM = "FLUENCY_LATAM"
    INTENSIVE = "INTENSIVE"
    B2B = "B2B"


class LeadStatus(str, enum.Enum):
    HOLDING = "HOLDING"
    CREATED = "CREATED"
    SALESFORCE_CREATED = "SALESFORCE_CREATED"
    INVALID_FORMAT = "INVALID_FORMAT"
    JOURNEY = "JOURNEY"
    DUPLICATED = "DUPLICATED"
    EXPIRED = "EXPIRED"
    FINISHED = "FINISHED"


class Journey(str, enum.Enum):
    LISTA_DE_ESPERA = "LISTA_DE_ESPERA"
    DOWNSELL = "DOWNSELL"
    BOLSA_DE_ESTUDOS = "BOLSA_DE_ESTUDOS"
    RESGATE = "RESGATE"


class JourneyStage(str, enum.Enum):
    PENDING = "PENDING"
    FIRST_CONTACT = "FIRST_CONTACT"
    LEAD_RESPONDED = "LEAD_RESPONDED"
    CONNECTION = "CONNECTION"
    DELIVERED = "DELIVERED"
    NEGOTIATION = "NEGOTIATION"
    LINK_SENT = "LINK_SENT"
    LOST = "LOST"
    WON = "WON"


class UpdateContact(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    custom_attributes: Optional[dict] = None
    event: Optional[str] = None
    changed_attributes: Optional[list] = None