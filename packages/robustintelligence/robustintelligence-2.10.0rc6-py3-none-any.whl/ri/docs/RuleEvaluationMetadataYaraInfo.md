# RuleEvaluationMetadataYaraInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_decisive_match** | **bool** | Whether we found a decisive YARA rule match. \&quot;decisive\&quot; means that the YARA result lead to a conclusive block or allow and we returned early in the detection pipeline. | [optional] 
**action** | [**GenerativefirewallFirewallAction**](GenerativefirewallFirewallAction.md) |  | [optional] 
**matched_by_rules** | **List[str]** | Which rules triggered on the text. | [optional] 

## Example

```python
from ri.fwclient.models.rule_evaluation_metadata_yara_info import RuleEvaluationMetadataYaraInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RuleEvaluationMetadataYaraInfo from a JSON string
rule_evaluation_metadata_yara_info_instance = RuleEvaluationMetadataYaraInfo.from_json(json)
# print the JSON string representation of the object
print(RuleEvaluationMetadataYaraInfo.to_json())

# convert the object into a dict
rule_evaluation_metadata_yara_info_dict = rule_evaluation_metadata_yara_info_instance.to_dict()
# create an instance of RuleEvaluationMetadataYaraInfo from a dict
rule_evaluation_metadata_yara_info_from_dict = RuleEvaluationMetadataYaraInfo.from_dict(rule_evaluation_metadata_yara_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

