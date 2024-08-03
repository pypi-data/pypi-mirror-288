# ArtifactIdentifierSubsetTestMetricIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_batch_id** | **str** | Uniquely specifies a Test Batch. | [optional] 
**metric** | **str** | The metric name. | [optional] 
**feature_names** | **List[str]** | Human-readable names of the features. Must be sorted lexicographically. | [optional] 
**subset_name** | **str** | Human-readable name of the feature subset used for the &#x60;subset_name&#x60; field. This is used to display the subset name on the frontend. | [optional] 

## Example

```python
from ri.apiclient.models.artifact_identifier_subset_test_metric_identifier import ArtifactIdentifierSubsetTestMetricIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ArtifactIdentifierSubsetTestMetricIdentifier from a JSON string
artifact_identifier_subset_test_metric_identifier_instance = ArtifactIdentifierSubsetTestMetricIdentifier.from_json(json)
# print the JSON string representation of the object
print(ArtifactIdentifierSubsetTestMetricIdentifier.to_json())

# convert the object into a dict
artifact_identifier_subset_test_metric_identifier_dict = artifact_identifier_subset_test_metric_identifier_instance.to_dict()
# create an instance of ArtifactIdentifierSubsetTestMetricIdentifier from a dict
artifact_identifier_subset_test_metric_identifier_from_dict = ArtifactIdentifierSubsetTestMetricIdentifier.from_dict(artifact_identifier_subset_test_metric_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

