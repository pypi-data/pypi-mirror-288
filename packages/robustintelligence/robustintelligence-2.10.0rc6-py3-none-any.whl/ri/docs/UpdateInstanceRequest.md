# UpdateInstanceRequest

Information about a single Firewall Instance, including its configuration and the current status of its deployment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_instance_id** | **object** | Unique ID of an object in RIME. | [optional] 
**config** | [**GenerativefirewallFirewallRuleConfig**](GenerativefirewallFirewallRuleConfig.md) |  | [optional] 
**deployment_status** | [**GenerativefirewallFirewallInstanceStatus**](GenerativefirewallFirewallInstanceStatus.md) |  | [optional] 
**description** | **str** | Optional human-readable description of the firewall instance. | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**spec** | [**GenerativefirewallFirewallInstanceDeploymentConfig**](GenerativefirewallFirewallInstanceDeploymentConfig.md) |  | [optional] 
**last_heartbeat_time** | **datetime** | Last time the control plan received a heartbeat from the firewall instance. | [optional] 

## Example

```python
from ri.fwclient.models.update_instance_request import UpdateInstanceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateInstanceRequest from a JSON string
update_instance_request_instance = UpdateInstanceRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateInstanceRequest.to_json())

# convert the object into a dict
update_instance_request_dict = update_instance_request_instance.to_dict()
# create an instance of UpdateInstanceRequest from a dict
update_instance_request_from_dict = UpdateInstanceRequest.from_dict(update_instance_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

