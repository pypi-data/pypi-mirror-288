# MonitorArtifactIdentifier

ArtifactIdentifier specifies the artifact a monitor tracks over time. Metrics exist in TestCases, TestBatches and CategoryTests. This is extendable to allow new kinds of metrics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_case_metric_identifier** | [**ArtifactIdentifierTestCaseMetricIdentifier**](ArtifactIdentifierTestCaseMetricIdentifier.md) |  | [optional] 
**category_test_metric_identifier** | [**ArtifactIdentifierCategoryTestIdentifier**](ArtifactIdentifierCategoryTestIdentifier.md) |  | [optional] 
**subset_test_metric_identifier** | [**ArtifactIdentifierSubsetTestMetricIdentifier**](ArtifactIdentifierSubsetTestMetricIdentifier.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.monitor_artifact_identifier import MonitorArtifactIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of MonitorArtifactIdentifier from a JSON string
monitor_artifact_identifier_instance = MonitorArtifactIdentifier.from_json(json)
# print the JSON string representation of the object
print(MonitorArtifactIdentifier.to_json())

# convert the object into a dict
monitor_artifact_identifier_dict = monitor_artifact_identifier_instance.to_dict()
# create an instance of MonitorArtifactIdentifier from a dict
monitor_artifact_identifier_from_dict = MonitorArtifactIdentifier.from_dict(monitor_artifact_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

