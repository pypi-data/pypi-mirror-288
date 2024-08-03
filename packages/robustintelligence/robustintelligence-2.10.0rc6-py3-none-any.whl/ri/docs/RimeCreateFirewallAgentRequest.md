# RimeCreateFirewallAgentRequest

CreateFirewallAgentRequest is the request for creating a firewall agent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The agent name given by the user. | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_firewall_agent_request import RimeCreateFirewallAgentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateFirewallAgentRequest from a JSON string
rime_create_firewall_agent_request_instance = RimeCreateFirewallAgentRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateFirewallAgentRequest.to_json())

# convert the object into a dict
rime_create_firewall_agent_request_dict = rime_create_firewall_agent_request_instance.to_dict()
# create an instance of RimeCreateFirewallAgentRequest from a dict
rime_create_firewall_agent_request_from_dict = RimeCreateFirewallAgentRequest.from_dict(rime_create_firewall_agent_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

