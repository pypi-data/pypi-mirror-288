# ListMetricIdentifiersResponseSubsetMetric


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metric_id** | [**ArtifactIdentifierSubsetTestMetricIdentifier**](ArtifactIdentifierSubsetTestMetricIdentifier.md) |  | [optional] 
**excluded_transforms** | [**MonitorExcludedTransforms**](MonitorExcludedTransforms.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.list_metric_identifiers_response_subset_metric import ListMetricIdentifiersResponseSubsetMetric

# TODO update the JSON string below
json = "{}"
# create an instance of ListMetricIdentifiersResponseSubsetMetric from a JSON string
list_metric_identifiers_response_subset_metric_instance = ListMetricIdentifiersResponseSubsetMetric.from_json(json)
# print the JSON string representation of the object
print(ListMetricIdentifiersResponseSubsetMetric.to_json())

# convert the object into a dict
list_metric_identifiers_response_subset_metric_dict = list_metric_identifiers_response_subset_metric_instance.to_dict()
# create an instance of ListMetricIdentifiersResponseSubsetMetric from a dict
list_metric_identifiers_response_subset_metric_from_dict = ListMetricIdentifiersResponseSubsetMetric.from_dict(list_metric_identifiers_response_subset_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

