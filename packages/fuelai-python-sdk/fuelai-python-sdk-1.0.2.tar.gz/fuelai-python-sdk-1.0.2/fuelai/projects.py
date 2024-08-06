import dateutil.parser
import datetime
import json

from fuelai.errors_extensions import FuelAIBackendError, FuelAIAPICredsMissingError, FuelAIRequiredParamError
from fuelai.api_client import ENDPOINTS, FuelAIAPIClient
from fuelai.tasks import Task
from fuelai.answers import Answer

class Project(FuelAIAPIClient):

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

        if not (hasattr(self, "orgProjectId") and self.orgProjectId):
            raise FuelAIRequiredParamError("orgProjectId")

        if not (hasattr(self, "name") and self.name):
            raise FuelAIRequiredParamError("name")

    def __str__(self):
        return f"<fuelai.Project#{self.orgProjectId} name=\"{self.name}\">"

    def __repr__(self):
        return f"<fuelai.Project={self.orgProjectId} name=\"{self.name}\" {self.attrs_repr()}>"

    def attrs_repr(self):
        return self.print_attributes(forbid_list=["name", "orgProjectId"])

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
    def create(cls,
               name: str,
               orgProjectId: str,
               orgTemplateId: str,
               raterInstructions: str = None,
               replication: int = 1,
               scrapingInfo: dict = None,
               api_key: str = None,
               api_secret: str = None):
        '''
        Creates a new Project.

        Arguments:
            name (str): Name of the project. Sometimes clients keep (name == orgProjectId)
            orgProjectId (str): The ID by which client identifies its project. Sometimes clients keep (name == orgProjectId)
            orgTemplateId (str): The ID of the template. This determines how the tasks and questions are rendered in front of the expert / rater. You might have to contact Fuel AI Team to get this.
            raterInstructions (str, optional): Instructions shown to experts / raters about how they should complete the task / question.
            replication (int, optional): How many replicas should be created of each task in this project. Replica=1 means 1 replication, i.e. only 1 expert / rater will submit the response
            scrapingInfo (dict, optional): Advanced options for creating a project where scraping a certain model is required.
            api_key (str): Override any set api_key
            api_secret (str): Override any set api_secret
        Returns:
            project: new Project object
        '''

        params = {
            'name': name,
            'orgProjectId': orgProjectId,
            'orgTemplateId': orgTemplateId,
            'raterInstructions': raterInstructions,
            'replication': replication,
        }
        if scrapingInfo is not None:
            params['scrapingInfo'] = { **scrapingInfo }
        response_json = cls.post(ENDPOINTS['PROJECT'], params, api_key=api_key, api_secret=api_secret)
        return cls(**response_json)

    @classmethod
    def getAll(cls, api_key: str = None, api_secret: str = None):
        response_json = cls.get(ENDPOINTS['PROJECTS'], {}, api_key=api_key, api_secret=api_secret)
        projects = [cls(**it) for it in response_json.get('projects', [])]
        return projects

    def uploadTasks(self, tasksRawArray: list, api_key: str = None, api_secret: str = None):
        self.tasks = Task.uploadTasks(self.orgProjectId, tasksRawArray, api_key, api_secret);
        return self.tasks;

    def getAllTasks(self, api_key: str = None, api_secret: str = None):
        self.tasks = Task.getAll(self.orgProjectId, api_key, api_secret);
        return self.tasks;

    def downloadAnswers(self, api_key: str = None, api_secret: str = None):
        self.answers = Answer.downloadAnswers(self.orgProjectId, api_key, api_secret);
        return self.answers;

