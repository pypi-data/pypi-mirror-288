# ListMetricIdentifiersResponseFeatureMetrics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_metric_without_subsets** | [**List[ListMetricIdentifiersResponseFeatureMetricWithoutSubsets]**](ListMetricIdentifiersResponseFeatureMetricWithoutSubsets.md) |  | [optional] 
**subset_metrics** | [**Dict[str, ListMetricIdentifiersResponseSubsetMetrics]**](ListMetricIdentifiersResponseSubsetMetrics.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.list_metric_identifiers_response_feature_metrics import ListMetricIdentifiersResponseFeatureMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of ListMetricIdentifiersResponseFeatureMetrics from a JSON string
list_metric_identifiers_response_feature_metrics_instance = ListMetricIdentifiersResponseFeatureMetrics.from_json(json)
# print the JSON string representation of the object
print(ListMetricIdentifiersResponseFeatureMetrics.to_json())

# convert the object into a dict
list_metric_identifiers_response_feature_metrics_dict = list_metric_identifiers_response_feature_metrics_instance.to_dict()
# create an instance of ListMetricIdentifiersResponseFeatureMetrics from a dict
list_metric_identifiers_response_feature_metrics_from_dict = ListMetricIdentifiersResponseFeatureMetrics.from_dict(list_metric_identifiers_response_feature_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

