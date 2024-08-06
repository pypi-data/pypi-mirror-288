import os

from fuelai.projects import Project
from fuelai.answers import Answer
from fuelai.tasks import Task

api_key = os.environ.get("FUELAI_API_KEY", None)
api_secret = os.environ.get("FUELAI_API_SECRET", None)
base_url = os.environ.get("FUELAI_BASE_URL", "https://apis.fuelhq.ai")
