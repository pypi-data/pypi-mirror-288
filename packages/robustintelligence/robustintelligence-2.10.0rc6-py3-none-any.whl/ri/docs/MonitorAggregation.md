# MonitorAggregation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregation_type** | [**MonitorAggregationType**](MonitorAggregationType.md) |  | [optional] 
**time_window** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.monitor_aggregation import MonitorAggregation

# TODO update the JSON string below
json = "{}"
# create an instance of MonitorAggregation from a JSON string
monitor_aggregation_instance = MonitorAggregation.from_json(json)
# print the JSON string representation of the object
print(MonitorAggregation.to_json())

# convert the object into a dict
monitor_aggregation_dict = monitor_aggregation_instance.to_dict()
# create an instance of MonitorAggregation from a dict
monitor_aggregation_from_dict = MonitorAggregation.from_dict(monitor_aggregation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

