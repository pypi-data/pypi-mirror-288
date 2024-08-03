# MonitorTransform


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**difference_from_target** | [**MonitorDifferenceFromTarget**](MonitorDifferenceFromTarget.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.monitor_transform import MonitorTransform

# TODO update the JSON string below
json = "{}"
# create an instance of MonitorTransform from a JSON string
monitor_transform_instance = MonitorTransform.from_json(json)
# print the JSON string representation of the object
print(MonitorTransform.to_json())

# convert the object into a dict
monitor_transform_dict = monitor_transform_instance.to_dict()
# create an instance of MonitorTransform from a dict
monitor_transform_from_dict = MonitorTransform.from_dict(monitor_transform_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

