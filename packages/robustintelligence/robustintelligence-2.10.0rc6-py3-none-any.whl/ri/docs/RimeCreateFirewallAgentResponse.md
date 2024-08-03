# RimeCreateFirewallAgentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**api_token** | **str** | The API token used by the agent for registration. | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_firewall_agent_response import RimeCreateFirewallAgentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateFirewallAgentResponse from a JSON string
rime_create_firewall_agent_response_instance = RimeCreateFirewallAgentResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateFirewallAgentResponse.to_json())

# convert the object into a dict
rime_create_firewall_agent_response_dict = rime_create_firewall_agent_response_instance.to_dict()
# create an instance of RimeCreateFirewallAgentResponse from a dict
rime_create_firewall_agent_response_from_dict = RimeCreateFirewallAgentResponse.from_dict(rime_create_firewall_agent_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

