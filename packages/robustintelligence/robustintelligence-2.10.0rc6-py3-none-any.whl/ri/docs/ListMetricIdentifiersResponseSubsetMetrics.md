# ListMetricIdentifiersResponseSubsetMetrics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metric_ids** | [**List[ListMetricIdentifiersResponseSubsetMetric]**](ListMetricIdentifiersResponseSubsetMetric.md) | List of Metric IDs. | [optional] 

## Example

```python
from ri.apiclient.models.list_metric_identifiers_response_subset_metrics import ListMetricIdentifiersResponseSubsetMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of ListMetricIdentifiersResponseSubsetMetrics from a JSON string
list_metric_identifiers_response_subset_metrics_instance = ListMetricIdentifiersResponseSubsetMetrics.from_json(json)
# print the JSON string representation of the object
print(ListMetricIdentifiersResponseSubsetMetrics.to_json())

# convert the object into a dict
list_metric_identifiers_response_subset_metrics_dict = list_metric_identifiers_response_subset_metrics_instance.to_dict()
# create an instance of ListMetricIdentifiersResponseSubsetMetrics from a dict
list_metric_identifiers_response_subset_metrics_from_dict = ListMetricIdentifiersResponseSubsetMetrics.from_dict(list_metric_identifiers_response_subset_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

