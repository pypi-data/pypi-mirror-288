# GenerativefirewallLanguageDetectionRuleConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**whitelisted_languages** | [**List[RimeLanguage]**](RimeLanguage.md) | Whitelisted languages are the languages that are allowed to be present in model input text. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_language_detection_rule_config import GenerativefirewallLanguageDetectionRuleConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallLanguageDetectionRuleConfig from a JSON string
generativefirewall_language_detection_rule_config_instance = GenerativefirewallLanguageDetectionRuleConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallLanguageDetectionRuleConfig.to_json())

# convert the object into a dict
generativefirewall_language_detection_rule_config_dict = generativefirewall_language_detection_rule_config_instance.to_dict()
# create an instance of GenerativefirewallLanguageDetectionRuleConfig from a dict
generativefirewall_language_detection_rule_config_from_dict = GenerativefirewallLanguageDetectionRuleConfig.from_dict(generativefirewall_language_detection_rule_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

