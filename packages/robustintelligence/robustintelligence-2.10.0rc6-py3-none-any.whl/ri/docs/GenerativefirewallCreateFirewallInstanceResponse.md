# GenerativefirewallCreateFirewallInstanceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_instance_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_create_firewall_instance_response import GenerativefirewallCreateFirewallInstanceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallCreateFirewallInstanceResponse from a JSON string
generativefirewall_create_firewall_instance_response_instance = GenerativefirewallCreateFirewallInstanceResponse.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallCreateFirewallInstanceResponse.to_json())

# convert the object into a dict
generativefirewall_create_firewall_instance_response_dict = generativefirewall_create_firewall_instance_response_instance.to_dict()
# create an instance of GenerativefirewallCreateFirewallInstanceResponse from a dict
generativefirewall_create_firewall_instance_response_from_dict = GenerativefirewallCreateFirewallInstanceResponse.from_dict(generativefirewall_create_firewall_instance_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

