import requests

import fuelai
from fuelai.errors_extensions import FuelAIBackendError, FuelAIAPICredsMissingError, FuelAIRequiredParamError, FuelAIInvalidConfigError

ENDPOINTS = {
    'PROJECT': '/apis/project',
    'PROJECTS': '/apis/projects',

    'TASKS': '/apis/tasks',

    'DOWNLOAD_ANSWERS': '/apis/download-answers',
}

def is_json(response):
    try:
        response.json()
        return True
    except ValueError:
        return False



def get_nested(data, *keys):
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data


class FuelAIAPIClient(object):

    def __init__(self, id=None):
        self.id = id

    def print_attributes(self, forbid_list: list = []):
        return " ".join([
            f"{k}=\"{v}\"" for k, v in self.__dict__.items() if not k in forbid_list
        ])

    @classmethod
    def _base_request(cls, method, api_endpoint, params=None, api_key=None, api_secret=None):
        api_key_to_use = api_key or fuelai.api_key
        api_secret_to_use = api_secret or fuelai.api_secret
        if api_key_to_use is None or api_secret_to_use is None:
            raise FuelAIAPICredsMissingError

        headers = {
            'api-key': api_key_to_use,
            'api-secret': api_secret_to_use,
            'content-type': 'application/json',
        }

        try:
            url = f"{fuelai.base_url}{api_endpoint}"

            # GET request
            if method == "get":
                response = requests.get(url, headers=headers, params=params)

            # POST request
            elif method == "post":
                response = requests.post(url, headers=headers, json=params)

            else:
                raise FuelAIInvalidConfigError(f'Invalid HTTP method. method={method}')

            # Raise exception if there is an http error
            response.raise_for_status()

            # If no errors, return response as json
            responseData = response.json()
            payload = responseData.get('payload', {})
            return payload;

        except requests.exceptions.HTTPError as httpError:
            # print(httpError);
            # print(f'Status code: {httpError.response.status_code}')  # Print the status code
            # print(f'HTTP error occurred: {httpError}')  # Print the error message
            if is_json(httpError.response):
                errorResponseData = httpError.response.json()
                # print(f'Error data: {errorResponseData}')  # Print the parsed JSON data
                errorMessage = errorResponseData.get('error', None)
                if errorMessage:
                    # print(f'Error message: {errorMessage}')  # Access the specific property
                    raise FuelAIBackendError(errorMessage) from None
            raise FuelAIBackendError from None

        except Exception:
            # Generic exception handling
            raise FuelAIBackendError

    @classmethod
    def get(cls, api_endpoint, params=None, api_key=None, api_secret=None):
        method = "get"
        return cls._base_request(method,
                                 api_endpoint,
                                 params=params,
                                 api_key=api_key,
                                 api_secret=api_secret)

    @classmethod
    def post(cls, api_endpoint, params=None, api_key=None, api_secret=None):
        method = "post"
        return cls._base_request(method,
                                 api_endpoint,
                                 params=params,
                                 api_key=api_key,
                                 api_secret=api_secret)
