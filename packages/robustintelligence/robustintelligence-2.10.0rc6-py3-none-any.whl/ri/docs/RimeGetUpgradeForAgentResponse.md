# RimeGetUpgradeForAgentResponse

GetUpgradeForAgentResponse is the response for GetUpgradeForAgent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**desired_state** | [**RimeAgentDesiredState**](RimeAgentDesiredState.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_upgrade_for_agent_response import RimeGetUpgradeForAgentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetUpgradeForAgentResponse from a JSON string
rime_get_upgrade_for_agent_response_instance = RimeGetUpgradeForAgentResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetUpgradeForAgentResponse.to_json())

# convert the object into a dict
rime_get_upgrade_for_agent_response_dict = rime_get_upgrade_for_agent_response_instance.to_dict()
# create an instance of RimeGetUpgradeForAgentResponse from a dict
rime_get_upgrade_for_agent_response_from_dict = RimeGetUpgradeForAgentResponse.from_dict(rime_get_upgrade_for_agent_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

