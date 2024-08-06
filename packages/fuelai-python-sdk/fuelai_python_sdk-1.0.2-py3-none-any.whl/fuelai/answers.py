import dateutil.parser
import datetime
import json

from fuelai.errors_extensions import FuelAIBackendError, FuelAIAPICredsMissingError, FuelAIRequiredParamError
from fuelai.api_client import ENDPOINTS, FuelAIAPIClient

class Answer(FuelAIAPIClient):

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"<fuelai.Answer>"

    def __repr__(self):
        return f"<fuelai.Answer {self.attrs_repr()}>"

    def attrs_repr(self):
        return self.print_attributes()

    def to_dict(self):
        return {
            key: self._to_dict_value(key, value)
            for key, value in self.__dict__.items() if not key.startswith('_')
        }

    def _to_dict_value(self, key, value):
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        else:
            return value

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def downloadAnswers(cls,
                        orgProjectId: str,
                        pageNo: int = None,
                        pageSize: int = None,
                        api_key: str = None,
                        api_secret: str = None):
        '''
        Download all the answers for you given orgProjectId.
        Please note it will download partial data also.
        Say out of given 100, 40 tasks are completed. This will download those 40 tasks.

        Arguments:
            orgProjectId (str): orgProjectId
            api_key (str): Override any set api_key
            api_secret (str): Override any set api_secret
        Returns:
            answers: Array of all the answers
        '''

        params = {
            'orgProjectId': orgProjectId,
            'pageNo': pageNo,
            'pageSize': pageSize,
        }
        response_json = cls.get(ENDPOINTS['DOWNLOAD_ANSWERS'], params, api_key=api_key, api_secret=api_secret)
        answers = [cls(**ans_json) for ans_json in response_json.get('data', [])]
        return answers

