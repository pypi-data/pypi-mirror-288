
class FuelAIBackendError(Exception):
    """A general exception for errors that arise during a request."""

    def __init__(self, message="Something went wrong with the API request."):
        self.message = message
        super().__init__(self.message)


class FuelAIAPICredsMissingError(Exception):
    """Raise when API key/secret is missing"""

    def __init__(self, message="FuelAI API_KEY and API_SECRET key has not been set."):
        self.message = message
        super().__init__(self.message)


class FuelAIInvalidConfigError(Exception):
    """Raise when config to call the API is not correct"""

    def __init__(self, message="Invalid Config Error"):
        self.message = message
        super().__init__(self.message)


class FuelAIRequiredParamError(Exception):
    """Raise when Required Param is missing"""

    def __init__(self, paramName):
        self.paramName = paramName
        self.message = f"{paramName} is a required attribute. Please set it."
        super().__init__(self.message)

