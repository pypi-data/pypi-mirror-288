# ArtifactIdentifierTestCaseMetricIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_batch_id** | **str** | Uniquely specifies a Test Batch. | [optional] 
**metric** | **str** | The metric name. | [optional] 
**feature_names** | **List[str]** | Human-readable names of the features. Must be sorted lexicographically. | [optional] 

## Example

```python
from ri.apiclient.models.artifact_identifier_test_case_metric_identifier import ArtifactIdentifierTestCaseMetricIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ArtifactIdentifierTestCaseMetricIdentifier from a JSON string
artifact_identifier_test_case_metric_identifier_instance = ArtifactIdentifierTestCaseMetricIdentifier.from_json(json)
# print the JSON string representation of the object
print(ArtifactIdentifierTestCaseMetricIdentifier.to_json())

# convert the object into a dict
artifact_identifier_test_case_metric_identifier_dict = artifact_identifier_test_case_metric_identifier_instance.to_dict()
# create an instance of ArtifactIdentifierTestCaseMetricIdentifier from a dict
artifact_identifier_test_case_metric_identifier_from_dict = ArtifactIdentifierTestCaseMetricIdentifier.from_dict(artifact_identifier_test_case_metric_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

