# GenerativefirewallUnknownExternalSourceRuleConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**whitelisted_urls** | **List[str]** | Whitelisted URLs is a list of the URL domains that should not be flagged by the unknown external source rule. | [optional] 
**ignore_contexts** | **bool** | Ignore contexts specifies whether the firewall should skip the contexts field of the model input in the firewall validate request. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_unknown_external_source_rule_config import GenerativefirewallUnknownExternalSourceRuleConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallUnknownExternalSourceRuleConfig from a JSON string
generativefirewall_unknown_external_source_rule_config_instance = GenerativefirewallUnknownExternalSourceRuleConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallUnknownExternalSourceRuleConfig.to_json())

# convert the object into a dict
generativefirewall_unknown_external_source_rule_config_dict = generativefirewall_unknown_external_source_rule_config_instance.to_dict()
# create an instance of GenerativefirewallUnknownExternalSourceRuleConfig from a dict
generativefirewall_unknown_external_source_rule_config_from_dict = GenerativefirewallUnknownExternalSourceRuleConfig.from_dict(generativefirewall_unknown_external_source_rule_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

