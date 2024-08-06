import dateutil.parser
import datetime
import json

from fuelai.errors_extensions import FuelAIBackendError, FuelAIAPICredsMissingError, FuelAIRequiredParamError
from fuelai.api_client import ENDPOINTS, FuelAIAPIClient

class Task(FuelAIAPIClient):

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

    def __str__(self):
        return f"<fuelai.Task>"

    def __repr__(self):
        return f"<fuelai.Task {self.attrs_repr()}>"

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
    def uploadTasks(cls,
                    orgProjectId: str,
                    tasksRawArray: list,
                    api_key: str = None,
                    api_secret: str = None):
        '''
        Upload Tasks for a given orgProjectId.

        Arguments:
            orgProjectId (str): orgProjectId
            tasksRawArray (list): Describing Task Details: Contact Fuel AI Team for struct. E.g: [{"orgTaskId":"H018","turns":[{"prompt":"What is the best way to learn AI?","file":null,"responses":[]}]}]
            api_key (str): Override any set api_key
            api_secret (str): Override any set api_secret
        Returns:
            answers: Array of all the answers
        '''

        params = {
            'orgProjectId': orgProjectId,
            'tasks': tasksRawArray,
        }
        response_json = cls.post(ENDPOINTS['TASKS'], params, api_key=api_key, api_secret=api_secret)
        tasks = [cls(**task_json) for task_json in response_json.get('tasks', [])]
        return tasks

    @classmethod
    def getAll(cls, orgProjectId: str, api_key: str = None, api_secret: str = None):
        '''
        Get All Tasks for a given orgProjectId.

        Arguments:
            orgProjectId (str): orgProjectId
            api_key (str): Override any set api_key
            api_secret (str): Override any set api_secret
        Returns:
            answers: Array of all the tasks
        '''
        response_json = cls.get(ENDPOINTS['TASKS'], { 'orgProjectId': orgProjectId }, api_key=api_key, api_secret=api_secret)
        tasks = [cls(**it) for it in response_json.get('tasks', [])]
        return tasks

