# RimeGetAgentResponse

GetAgentResponse is the response returns a single agent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent** | [**RimeAgent**](RimeAgent.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_agent_response import RimeGetAgentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetAgentResponse from a JSON string
rime_get_agent_response_instance = RimeGetAgentResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetAgentResponse.to_json())

# convert the object into a dict
rime_get_agent_response_dict = rime_get_agent_response_instance.to_dict()
# create an instance of RimeGetAgentResponse from a dict
rime_get_agent_response_from_dict = RimeGetAgentResponse.from_dict(rime_get_agent_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

