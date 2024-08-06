# Fuel AI Python SDK

This Fuel AI Python SDK gives easy access to the Fuel AI Backend APIs.

## Installation

Install this package by using pip:

```bash
pip install --upgrade fuelai-python-sdk
```

### Requirements

* Python 3.6+

### Authentication

The library needs to be configured with your account's API KEY and API SECRET which is available in your Fuel AI Account - [https://fuelhq.ai/dashboard/apis](https://fuelhq.ai/dashboard/apis). Set `fuelai.api_key` and `fuelai.api_secret` to its value:

```python
import fuelai
fuelai.api_key = "YOUR API KEY"
fuelai.api_secret = "YOUR API SECRET"
```
Or set the API key as an environment variable:

```bash
export FUELAI_API_KEY=<YOUR API KEY>
export FUELAI_API_SECRET=<YOUR API SECRET>
```

### Projects
Once the API key has been set, you can use all the APIs

```python
# Create Project
new_project = fuelai.Project.create(name='NAME TO IDENTIFY',
                                    orgProjectId='ID TO IDENTIFY (MAYBE SAME AS NAME)',
                                    orgTemplateId='TEMPLATE ID - CONTACT FUEL AI TEAM FOR THIS')

print(new_project)
```


### Download Answers
Download Answers of the project. Please note that if out of 100 tasks, 40 are done, this API will download the 40 responses.

```python
# Download Answers
answers = fuelai.Answer.downloadAnswers(orgProjectId)
print(answers)
```
