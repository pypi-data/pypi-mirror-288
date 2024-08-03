# MonitorDifferenceFromTarget

DifferenceFromTarget defines a transform that calculates the difference between the aggregated metric defined in the monitor and the same metric defined with the target. if no aggregation is specified, an average value is used.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**difference** | [**DifferenceFromTargetDifference**](DifferenceFromTargetDifference.md) |  | [optional] 
**target** | [**DifferenceFromTargetTarget**](DifferenceFromTargetTarget.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.monitor_difference_from_target import MonitorDifferenceFromTarget

# TODO update the JSON string below
json = "{}"
# create an instance of MonitorDifferenceFromTarget from a JSON string
monitor_difference_from_target_instance = MonitorDifferenceFromTarget.from_json(json)
# print the JSON string representation of the object
print(MonitorDifferenceFromTarget.to_json())

# convert the object into a dict
monitor_difference_from_target_dict = monitor_difference_from_target_instance.to_dict()
# create an instance of MonitorDifferenceFromTarget from a dict
monitor_difference_from_target_from_dict = MonitorDifferenceFromTarget.from_dict(monitor_difference_from_target_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

