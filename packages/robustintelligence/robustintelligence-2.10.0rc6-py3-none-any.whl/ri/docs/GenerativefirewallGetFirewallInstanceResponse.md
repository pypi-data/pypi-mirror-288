# GenerativefirewallGetFirewallInstanceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_instance** | [**GenerativefirewallFirewallInstanceInfo**](GenerativefirewallFirewallInstanceInfo.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_get_firewall_instance_response import GenerativefirewallGetFirewallInstanceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallGetFirewallInstanceResponse from a JSON string
generativefirewall_get_firewall_instance_response_instance = GenerativefirewallGetFirewallInstanceResponse.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallGetFirewallInstanceResponse.to_json())

# convert the object into a dict
generativefirewall_get_firewall_instance_response_dict = generativefirewall_get_firewall_instance_response_instance.to_dict()
# create an instance of GenerativefirewallGetFirewallInstanceResponse from a dict
generativefirewall_get_firewall_instance_response_from_dict = GenerativefirewallGetFirewallInstanceResponse.from_dict(generativefirewall_get_firewall_instance_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

