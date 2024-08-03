# GenerativefirewallCreateFirewallInstanceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | [**GenerativefirewallFirewallRuleConfig**](GenerativefirewallFirewallRuleConfig.md) |  | [optional] 
**description** | **str** | Optional human-readable description of the firewall instance. | [optional] 
**spec** | [**GenerativefirewallFirewallInstanceDeploymentConfig**](GenerativefirewallFirewallInstanceDeploymentConfig.md) |  | [optional] 
**firewall_instance_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_create_firewall_instance_request import GenerativefirewallCreateFirewallInstanceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallCreateFirewallInstanceRequest from a JSON string
generativefirewall_create_firewall_instance_request_instance = GenerativefirewallCreateFirewallInstanceRequest.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallCreateFirewallInstanceRequest.to_json())

# convert the object into a dict
generativefirewall_create_firewall_instance_request_dict = generativefirewall_create_firewall_instance_request_instance.to_dict()
# create an instance of GenerativefirewallCreateFirewallInstanceRequest from a dict
generativefirewall_create_firewall_instance_request_from_dict = GenerativefirewallCreateFirewallInstanceRequest.from_dict(generativefirewall_create_firewall_instance_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

