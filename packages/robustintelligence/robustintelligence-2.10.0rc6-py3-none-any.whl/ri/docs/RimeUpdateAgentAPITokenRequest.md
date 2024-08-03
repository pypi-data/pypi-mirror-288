# RimeUpdateAgentAPITokenRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_update_agent_api_token_request import RimeUpdateAgentAPITokenRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUpdateAgentAPITokenRequest from a JSON string
rime_update_agent_api_token_request_instance = RimeUpdateAgentAPITokenRequest.from_json(json)
# print the JSON string representation of the object
print(RimeUpdateAgentAPITokenRequest.to_json())

# convert the object into a dict
rime_update_agent_api_token_request_dict = rime_update_agent_api_token_request_instance.to_dict()
# create an instance of RimeUpdateAgentAPITokenRequest from a dict
rime_update_agent_api_token_request_from_dict = RimeUpdateAgentAPITokenRequest.from_dict(rime_update_agent_api_token_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

