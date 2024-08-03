# RequestFirewallInstanceRequest

RequestFirewallInstanceRequest is the request to ask a firewall agent to create a firewall instance (via the CP).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | **object** | ID of the agent that will create the firewall instance. | [optional] 
**config** | [**GenerativefirewallFirewallRuleConfig**](GenerativefirewallFirewallRuleConfig.md) |  | [optional] 
**description** | **str** | Optional human-readable description of the firewall instance. | [optional] 
**spec** | [**GenerativefirewallFirewallInstanceDeploymentConfig**](GenerativefirewallFirewallInstanceDeploymentConfig.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.request_firewall_instance_request import RequestFirewallInstanceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RequestFirewallInstanceRequest from a JSON string
request_firewall_instance_request_instance = RequestFirewallInstanceRequest.from_json(json)
# print the JSON string representation of the object
print(RequestFirewallInstanceRequest.to_json())

# convert the object into a dict
request_firewall_instance_request_dict = request_firewall_instance_request_instance.to_dict()
# create an instance of RequestFirewallInstanceRequest from a dict
request_firewall_instance_request_from_dict = RequestFirewallInstanceRequest.from_dict(request_firewall_instance_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

