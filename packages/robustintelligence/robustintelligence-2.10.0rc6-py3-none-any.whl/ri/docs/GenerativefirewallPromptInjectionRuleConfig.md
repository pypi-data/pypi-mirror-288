# GenerativefirewallPromptInjectionRuleConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt_injection_rule_sensitivity** | [**GenerativefirewallRuleSensitivity**](GenerativefirewallRuleSensitivity.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_prompt_injection_rule_config import GenerativefirewallPromptInjectionRuleConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallPromptInjectionRuleConfig from a JSON string
generativefirewall_prompt_injection_rule_config_instance = GenerativefirewallPromptInjectionRuleConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallPromptInjectionRuleConfig.to_json())

# convert the object into a dict
generativefirewall_prompt_injection_rule_config_dict = generativefirewall_prompt_injection_rule_config_instance.to_dict()
# create an instance of GenerativefirewallPromptInjectionRuleConfig from a dict
generativefirewall_prompt_injection_rule_config_from_dict = GenerativefirewallPromptInjectionRuleConfig.from_dict(generativefirewall_prompt_injection_rule_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

