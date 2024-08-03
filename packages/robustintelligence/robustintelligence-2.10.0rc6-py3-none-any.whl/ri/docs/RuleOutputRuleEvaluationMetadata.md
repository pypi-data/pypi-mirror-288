# RuleOutputRuleEvaluationMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**evaluation_models** | [**Dict[str, RuleEvaluationMetadataModelInfo]**](RuleEvaluationMetadataModelInfo.md) | Map from the name of the model (&#x60;prompt-injection&#x60;, &#x60;toxicity&#x60;) to information about how it was used in evaluation. | [optional] 
**yara_hotfix** | [**RuleEvaluationMetadataYaraInfo**](RuleEvaluationMetadataYaraInfo.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.rule_output_rule_evaluation_metadata import RuleOutputRuleEvaluationMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of RuleOutputRuleEvaluationMetadata from a JSON string
rule_output_rule_evaluation_metadata_instance = RuleOutputRuleEvaluationMetadata.from_json(json)
# print the JSON string representation of the object
print(RuleOutputRuleEvaluationMetadata.to_json())

# convert the object into a dict
rule_output_rule_evaluation_metadata_dict = rule_output_rule_evaluation_metadata_instance.to_dict()
# create an instance of RuleOutputRuleEvaluationMetadata from a dict
rule_output_rule_evaluation_metadata_from_dict = RuleOutputRuleEvaluationMetadata.from_dict(rule_output_rule_evaluation_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

