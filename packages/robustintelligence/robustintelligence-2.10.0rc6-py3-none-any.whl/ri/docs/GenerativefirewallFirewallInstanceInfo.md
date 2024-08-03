# GenerativefirewallFirewallInstanceInfo

Information about a single Firewall Instance, including its configuration and the current status of its deployment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_instance_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**config** | [**GenerativefirewallFirewallRuleConfig**](GenerativefirewallFirewallRuleConfig.md) |  | [optional] 
**deployment_status** | [**GenerativefirewallFirewallInstanceStatus**](GenerativefirewallFirewallInstanceStatus.md) |  | [optional] 
**description** | **str** | Optional human-readable description of the firewall instance. | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**spec** | [**GenerativefirewallFirewallInstanceDeploymentConfig**](GenerativefirewallFirewallInstanceDeploymentConfig.md) |  | [optional] 
**last_heartbeat_time** | **datetime** | Last time the control plan received a heartbeat from the firewall instance. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_firewall_instance_info import GenerativefirewallFirewallInstanceInfo

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallFirewallInstanceInfo from a JSON string
generativefirewall_firewall_instance_info_instance = GenerativefirewallFirewallInstanceInfo.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallFirewallInstanceInfo.to_json())

# convert the object into a dict
generativefirewall_firewall_instance_info_dict = generativefirewall_firewall_instance_info_instance.to_dict()
# create an instance of GenerativefirewallFirewallInstanceInfo from a dict
generativefirewall_firewall_instance_info_from_dict = GenerativefirewallFirewallInstanceInfo.from_dict(generativefirewall_firewall_instance_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

