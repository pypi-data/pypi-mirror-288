# GenerativefirewallToxicityRuleConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**toxicity_rule_sensitivity** | [**GenerativefirewallRuleSensitivity**](GenerativefirewallRuleSensitivity.md) |  | [optional] 
**toxicity_rule_mode** | [**GenerativefirewallToxicityRuleMode**](GenerativefirewallToxicityRuleMode.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_toxicity_rule_config import GenerativefirewallToxicityRuleConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallToxicityRuleConfig from a JSON string
generativefirewall_toxicity_rule_config_instance = GenerativefirewallToxicityRuleConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallToxicityRuleConfig.to_json())

# convert the object into a dict
generativefirewall_toxicity_rule_config_dict = generativefirewall_toxicity_rule_config_instance.to_dict()
# create an instance of GenerativefirewallToxicityRuleConfig from a dict
generativefirewall_toxicity_rule_config_from_dict = GenerativefirewallToxicityRuleConfig.from_dict(generativefirewall_toxicity_rule_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

