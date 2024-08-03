# RimeUpdateAgentAPITokenResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**full_api_token** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_update_agent_api_token_response import RimeUpdateAgentAPITokenResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUpdateAgentAPITokenResponse from a JSON string
rime_update_agent_api_token_response_instance = RimeUpdateAgentAPITokenResponse.from_json(json)
# print the JSON string representation of the object
print(RimeUpdateAgentAPITokenResponse.to_json())

# convert the object into a dict
rime_update_agent_api_token_response_dict = rime_update_agent_api_token_response_instance.to_dict()
# create an instance of RimeUpdateAgentAPITokenResponse from a dict
rime_update_agent_api_token_response_from_dict = RimeUpdateAgentAPITokenResponse.from_dict(rime_update_agent_api_token_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

