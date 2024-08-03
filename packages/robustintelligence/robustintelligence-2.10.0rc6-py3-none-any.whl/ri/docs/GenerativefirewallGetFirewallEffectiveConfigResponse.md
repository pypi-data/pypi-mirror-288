# GenerativefirewallGetFirewallEffectiveConfigResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | [**GenerativefirewallFirewallRuleConfig**](GenerativefirewallFirewallRuleConfig.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_get_firewall_effective_config_response import GenerativefirewallGetFirewallEffectiveConfigResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallGetFirewallEffectiveConfigResponse from a JSON string
generativefirewall_get_firewall_effective_config_response_instance = GenerativefirewallGetFirewallEffectiveConfigResponse.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallGetFirewallEffectiveConfigResponse.to_json())

# convert the object into a dict
generativefirewall_get_firewall_effective_config_response_dict = generativefirewall_get_firewall_effective_config_response_instance.to_dict()
# create an instance of GenerativefirewallGetFirewallEffectiveConfigResponse from a dict
generativefirewall_get_firewall_effective_config_response_from_dict = GenerativefirewallGetFirewallEffectiveConfigResponse.from_dict(generativefirewall_get_firewall_effective_config_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

