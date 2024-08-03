# GenerativefirewallIndividualRulesConfig

IndividualRulesConfig contains configuration parameters for each individual rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**off_topic** | [**GenerativefirewallOffTopicRuleConfig**](GenerativefirewallOffTopicRuleConfig.md) |  | [optional] 
**pii_detection_input** | [**GenerativefirewallPiiDetectionRuleConfig**](GenerativefirewallPiiDetectionRuleConfig.md) |  | [optional] 
**pii_detection_output** | [**GenerativefirewallPiiDetectionRuleConfig**](GenerativefirewallPiiDetectionRuleConfig.md) |  | [optional] 
**token_counter_input** | [**GenerativefirewallTokenCounterRuleConfig**](GenerativefirewallTokenCounterRuleConfig.md) |  | [optional] 
**token_counter_output** | [**GenerativefirewallTokenCounterRuleConfig**](GenerativefirewallTokenCounterRuleConfig.md) |  | [optional] 
**unknown_external_source** | [**GenerativefirewallUnknownExternalSourceRuleConfig**](GenerativefirewallUnknownExternalSourceRuleConfig.md) |  | [optional] 
**language_detection** | [**GenerativefirewallLanguageDetectionRuleConfig**](GenerativefirewallLanguageDetectionRuleConfig.md) |  | [optional] 
**prompt_injection** | [**GenerativefirewallPromptInjectionRuleConfig**](GenerativefirewallPromptInjectionRuleConfig.md) |  | [optional] 
**toxicity_rule_config_input** | [**GenerativefirewallToxicityRuleConfig**](GenerativefirewallToxicityRuleConfig.md) |  | [optional] 
**toxicity_rule_config_output** | [**GenerativefirewallToxicityRuleConfig**](GenerativefirewallToxicityRuleConfig.md) |  | [optional] 
**code_detection** | [**GenerativefirewallCodeDetectionRuleConfig**](GenerativefirewallCodeDetectionRuleConfig.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_individual_rules_config import GenerativefirewallIndividualRulesConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallIndividualRulesConfig from a JSON string
generativefirewall_individual_rules_config_instance = GenerativefirewallIndividualRulesConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallIndividualRulesConfig.to_json())

# convert the object into a dict
generativefirewall_individual_rules_config_dict = generativefirewall_individual_rules_config_instance.to_dict()
# create an instance of GenerativefirewallIndividualRulesConfig from a dict
generativefirewall_individual_rules_config_from_dict = GenerativefirewallIndividualRulesConfig.from_dict(generativefirewall_individual_rules_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

