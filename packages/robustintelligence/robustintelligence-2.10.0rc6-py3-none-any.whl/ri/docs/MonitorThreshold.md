# MonitorThreshold


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**low** | **float** | The threshold for warning. | [optional] 
**high** | **float** | The threshold for alert. | [optional] 
**type** | [**MonitorThresholdType**](MonitorThresholdType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.monitor_threshold import MonitorThreshold

# TODO update the JSON string below
json = "{}"
# create an instance of MonitorThreshold from a JSON string
monitor_threshold_instance = MonitorThreshold.from_json(json)
# print the JSON string representation of the object
print(MonitorThreshold.to_json())

# convert the object into a dict
monitor_threshold_dict = monitor_threshold_instance.to_dict()
# create an instance of MonitorThreshold from a dict
monitor_threshold_from_dict = MonitorThreshold.from_dict(monitor_threshold_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

