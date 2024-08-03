# GenerativefirewallUpdateFirewallInstanceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**updated_firewall_instance** | [**GenerativefirewallFirewallInstanceInfo**](GenerativefirewallFirewallInstanceInfo.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_update_firewall_instance_response import GenerativefirewallUpdateFirewallInstanceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallUpdateFirewallInstanceResponse from a JSON string
generativefirewall_update_firewall_instance_response_instance = GenerativefirewallUpdateFirewallInstanceResponse.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallUpdateFirewallInstanceResponse.to_json())

# convert the object into a dict
generativefirewall_update_firewall_instance_response_dict = generativefirewall_update_firewall_instance_response_instance.to_dict()
# create an instance of GenerativefirewallUpdateFirewallInstanceResponse from a dict
generativefirewall_update_firewall_instance_response_from_dict = GenerativefirewallUpdateFirewallInstanceResponse.from_dict(generativefirewall_update_firewall_instance_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

