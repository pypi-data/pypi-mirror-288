# ListMetricIdentifiersResponseAggregatedMetric


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_case_metric_id** | [**ArtifactIdentifierTestCaseMetricIdentifier**](ArtifactIdentifierTestCaseMetricIdentifier.md) |  | [optional] 
**category_test_metric_id** | [**ArtifactIdentifierCategoryTestIdentifier**](ArtifactIdentifierCategoryTestIdentifier.md) |  | [optional] 
**excluded_transforms** | [**MonitorExcludedTransforms**](MonitorExcludedTransforms.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.list_metric_identifiers_response_aggregated_metric import ListMetricIdentifiersResponseAggregatedMetric

# TODO update the JSON string below
json = "{}"
# create an instance of ListMetricIdentifiersResponseAggregatedMetric from a JSON string
list_metric_identifiers_response_aggregated_metric_instance = ListMetricIdentifiersResponseAggregatedMetric.from_json(json)
# print the JSON string representation of the object
print(ListMetricIdentifiersResponseAggregatedMetric.to_json())

# convert the object into a dict
list_metric_identifiers_response_aggregated_metric_dict = list_metric_identifiers_response_aggregated_metric_instance.to_dict()
# create an instance of ListMetricIdentifiersResponseAggregatedMetric from a dict
list_metric_identifiers_response_aggregated_metric_from_dict = ListMetricIdentifiersResponseAggregatedMetric.from_dict(list_metric_identifiers_response_aggregated_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

