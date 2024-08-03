# ListMetricIdentifiersResponseFeatureMetricWithoutSubsets


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_case_metric_identifier** | [**ArtifactIdentifierTestCaseMetricIdentifier**](ArtifactIdentifierTestCaseMetricIdentifier.md) |  | [optional] 
**excluded_transforms** | [**MonitorExcludedTransforms**](MonitorExcludedTransforms.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.list_metric_identifiers_response_feature_metric_without_subsets import ListMetricIdentifiersResponseFeatureMetricWithoutSubsets

# TODO update the JSON string below
json = "{}"
# create an instance of ListMetricIdentifiersResponseFeatureMetricWithoutSubsets from a JSON string
list_metric_identifiers_response_feature_metric_without_subsets_instance = ListMetricIdentifiersResponseFeatureMetricWithoutSubsets.from_json(json)
# print the JSON string representation of the object
print(ListMetricIdentifiersResponseFeatureMetricWithoutSubsets.to_json())

# convert the object into a dict
list_metric_identifiers_response_feature_metric_without_subsets_dict = list_metric_identifiers_response_feature_metric_without_subsets_instance.to_dict()
# create an instance of ListMetricIdentifiersResponseFeatureMetricWithoutSubsets from a dict
list_metric_identifiers_response_feature_metric_without_subsets_from_dict = ListMetricIdentifiersResponseFeatureMetricWithoutSubsets.from_dict(list_metric_identifiers_response_feature_metric_without_subsets_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

