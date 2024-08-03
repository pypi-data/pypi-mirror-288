# RimeListMetricIdentifiersResponse

ListMetricIdentifiersResponse returns metric identifiers grouped under features, subsets or neither.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregated_metrics** | [**List[ListMetricIdentifiersResponseAggregatedMetric]**](ListMetricIdentifiersResponseAggregatedMetric.md) |  | [optional] 
**feature_metrics** | [**Dict[str, ListMetricIdentifiersResponseFeatureMetrics]**](ListMetricIdentifiersResponseFeatureMetrics.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_metric_identifiers_response import RimeListMetricIdentifiersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListMetricIdentifiersResponse from a JSON string
rime_list_metric_identifiers_response_instance = RimeListMetricIdentifiersResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListMetricIdentifiersResponse.to_json())

# convert the object into a dict
rime_list_metric_identifiers_response_dict = rime_list_metric_identifiers_response_instance.to_dict()
# create an instance of RimeListMetricIdentifiersResponse from a dict
rime_list_metric_identifiers_response_from_dict = RimeListMetricIdentifiersResponse.from_dict(rime_list_metric_identifiers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

