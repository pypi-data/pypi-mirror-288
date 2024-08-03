# UpgradeAgentRequest

UpgradeAgentRequest is the request for upgrading an agent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | **object** | Uniquely specifies an Agent. | [optional] 
**custom_values** | **Dict[str, str]** | Example:   {     \&quot;rimeAgent.images.agentImage.registry\&quot;: \&quot;docker.io\&quot;,   } | [optional] 

## Example

```python
from ri.apiclient.models.upgrade_agent_request import UpgradeAgentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpgradeAgentRequest from a JSON string
upgrade_agent_request_instance = UpgradeAgentRequest.from_json(json)
# print the JSON string representation of the object
print(UpgradeAgentRequest.to_json())

# convert the object into a dict
upgrade_agent_request_dict = upgrade_agent_request_instance.to_dict()
# create an instance of UpgradeAgentRequest from a dict
upgrade_agent_request_from_dict = UpgradeAgentRequest.from_dict(upgrade_agent_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

