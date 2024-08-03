# RimeRegisterExternalAgentRequest

RegisterExternalAgentRequest is sent as part of external agent startup.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**signing_key** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_register_external_agent_request import RimeRegisterExternalAgentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeRegisterExternalAgentRequest from a JSON string
rime_register_external_agent_request_instance = RimeRegisterExternalAgentRequest.from_json(json)
# print the JSON string representation of the object
print(RimeRegisterExternalAgentRequest.to_json())

# convert the object into a dict
rime_register_external_agent_request_dict = rime_register_external_agent_request_instance.to_dict()
# create an instance of RimeRegisterExternalAgentRequest from a dict
rime_register_external_agent_request_from_dict = RimeRegisterExternalAgentRequest.from_dict(rime_register_external_agent_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

