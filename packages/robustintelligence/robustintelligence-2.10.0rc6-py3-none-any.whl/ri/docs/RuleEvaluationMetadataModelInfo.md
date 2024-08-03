# RuleEvaluationMetadataModelInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_version** | **str** |  | [optional] 
**chunk_scores** | [**List[GenerativefirewallRawModelPrediction]**](GenerativefirewallRawModelPrediction.md) | List of model scores for each chunk in the input; we perform chunking because our models can process a fixed number of tokens in a single inference. Sorted in ascending order by chunk index. | [optional] 

## Example

```python
from ri.fwclient.models.rule_evaluation_metadata_model_info import RuleEvaluationMetadataModelInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RuleEvaluationMetadataModelInfo from a JSON string
rule_evaluation_metadata_model_info_instance = RuleEvaluationMetadataModelInfo.from_json(json)
# print the JSON string representation of the object
print(RuleEvaluationMetadataModelInfo.to_json())

# convert the object into a dict
rule_evaluation_metadata_model_info_dict = rule_evaluation_metadata_model_info_instance.to_dict()
# create an instance of RuleEvaluationMetadataModelInfo from a dict
rule_evaluation_metadata_model_info_from_dict = RuleEvaluationMetadataModelInfo.from_dict(rule_evaluation_metadata_model_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

