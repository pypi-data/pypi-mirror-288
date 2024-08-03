# GenerativefirewallPiiDetectionRuleConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**entity_types** | [**List[GenerativefirewallPiiEntityType]**](GenerativefirewallPiiEntityType.md) | Entity types determines which types of PII will be flagged. | [optional] 
**custom_entities** | [**List[GenerativefirewallCustomPiiEntity]**](GenerativefirewallCustomPiiEntity.md) | Custom entities are custom-specified patterns to flag. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_pii_detection_rule_config import GenerativefirewallPiiDetectionRuleConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallPiiDetectionRuleConfig from a JSON string
generativefirewall_pii_detection_rule_config_instance = GenerativefirewallPiiDetectionRuleConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallPiiDetectionRuleConfig.to_json())

# convert the object into a dict
generativefirewall_pii_detection_rule_config_dict = generativefirewall_pii_detection_rule_config_instance.to_dict()
# create an instance of GenerativefirewallPiiDetectionRuleConfig from a dict
generativefirewall_pii_detection_rule_config_from_dict = GenerativefirewallPiiDetectionRuleConfig.from_dict(generativefirewall_pii_detection_rule_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

