# GenerativefirewallFirewallRuleConfig

FirewallRuleConfig describes the firewall rule configuration of the firewall.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**language** | [**RimeLanguage**](RimeLanguage.md) |  | [optional] 
**selected_rules** | [**List[GenerativefirewallFirewallRuleType]**](GenerativefirewallFirewallRuleType.md) | If this list is empty, all available firewall rules will be run. Otherwise, only the rules specified here will be run. | [optional] 
**individual_rules_config** | [**GenerativefirewallIndividualRulesConfig**](GenerativefirewallIndividualRulesConfig.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_firewall_rule_config import GenerativefirewallFirewallRuleConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallFirewallRuleConfig from a JSON string
generativefirewall_firewall_rule_config_instance = GenerativefirewallFirewallRuleConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallFirewallRuleConfig.to_json())

# convert the object into a dict
generativefirewall_firewall_rule_config_dict = generativefirewall_firewall_rule_config_instance.to_dict()
# create an instance of GenerativefirewallFirewallRuleConfig from a dict
generativefirewall_firewall_rule_config_from_dict = GenerativefirewallFirewallRuleConfig.from_dict(generativefirewall_firewall_rule_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

