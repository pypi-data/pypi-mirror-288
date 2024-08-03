# MonitorExcludedTransforms

ExcludedTransforms allows a metric to define which transforms cannot be applied to the metric.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**excluded_transforms** | [**List[MonitorTransform]**](MonitorTransform.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.monitor_excluded_transforms import MonitorExcludedTransforms

# TODO update the JSON string below
json = "{}"
# create an instance of MonitorExcludedTransforms from a JSON string
monitor_excluded_transforms_instance = MonitorExcludedTransforms.from_json(json)
# print the JSON string representation of the object
print(MonitorExcludedTransforms.to_json())

# convert the object into a dict
monitor_excluded_transforms_dict = monitor_excluded_transforms_instance.to_dict()
# create an instance of MonitorExcludedTransforms from a dict
monitor_excluded_transforms_from_dict = MonitorExcludedTransforms.from_dict(monitor_excluded_transforms_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

