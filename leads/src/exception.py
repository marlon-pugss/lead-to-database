class FluencyLeadException(Exception):
    pass


class SalesforceException(FluencyLeadException):
    pass


class CreateLeadException(FluencyLeadException):
    pass


class NotFoundException(FluencyLeadException):
    pass


class MissingRequiredAttributeException(Exception):
    """Raised when a required attribute is missing from an object."""
    pass


class LeadSourceConfigurationException(FluencyLeadException):
    pass