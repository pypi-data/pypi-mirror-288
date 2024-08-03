# GenerativefirewallOffTopicRuleConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**in_domain_intents** | **List[str]** | In_domain_intents is a list of strings that are considered on-topic. Total number of data points in in_domain_intents and restricted_intents should not exceed 500 and total bytes should not exceed 300KB. | [optional] 
**restricted_intents** | **List[str]** |  | [optional] 
**in_domain_intents_sensitivity** | [**GenerativefirewallRuleSensitivity**](GenerativefirewallRuleSensitivity.md) |  | [optional] 
**restricted_intents_sensitivity** | [**GenerativefirewallRuleSensitivity**](GenerativefirewallRuleSensitivity.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_off_topic_rule_config import GenerativefirewallOffTopicRuleConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallOffTopicRuleConfig from a JSON string
generativefirewall_off_topic_rule_config_instance = GenerativefirewallOffTopicRuleConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallOffTopicRuleConfig.to_json())

# convert the object into a dict
generativefirewall_off_topic_rule_config_dict = generativefirewall_off_topic_rule_config_instance.to_dict()
# create an instance of GenerativefirewallOffTopicRuleConfig from a dict
generativefirewall_off_topic_rule_config_from_dict = GenerativefirewallOffTopicRuleConfig.from_dict(generativefirewall_off_topic_rule_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

