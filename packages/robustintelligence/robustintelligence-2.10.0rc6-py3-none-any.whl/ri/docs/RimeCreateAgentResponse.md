# RimeCreateAgentResponse

CreateAgentResponse is a response that contains the configuration values required for installing the agent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | **bytearray** | File that contains configuration values for installing the agent. | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_agent_response import RimeCreateAgentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateAgentResponse from a JSON string
rime_create_agent_response_instance = RimeCreateAgentResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateAgentResponse.to_json())

# convert the object into a dict
rime_create_agent_response_dict = rime_create_agent_response_instance.to_dict()
# create an instance of RimeCreateAgentResponse from a dict
rime_create_agent_response_from_dict = RimeCreateAgentResponse.from_dict(rime_create_agent_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

