# GenerativefirewallListFirewallInstancesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_instances** | [**List[GenerativefirewallFirewallInstanceInfo]**](GenerativefirewallFirewallInstanceInfo.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_list_firewall_instances_response import GenerativefirewallListFirewallInstancesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallListFirewallInstancesResponse from a JSON string
generativefirewall_list_firewall_instances_response_instance = GenerativefirewallListFirewallInstancesResponse.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallListFirewallInstancesResponse.to_json())

# convert the object into a dict
generativefirewall_list_firewall_instances_response_dict = generativefirewall_list_firewall_instances_response_instance.to_dict()
# create an instance of GenerativefirewallListFirewallInstancesResponse from a dict
generativefirewall_list_firewall_instances_response_from_dict = GenerativefirewallListFirewallInstancesResponse.from_dict(generativefirewall_list_firewall_instances_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

