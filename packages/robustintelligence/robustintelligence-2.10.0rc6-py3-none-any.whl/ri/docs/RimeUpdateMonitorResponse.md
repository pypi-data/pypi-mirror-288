# RimeUpdateMonitorResponse

UpdateMonitorResponse returns the updated monitor.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**monitor** | [**MonitorMonitor**](MonitorMonitor.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_update_monitor_response import RimeUpdateMonitorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUpdateMonitorResponse from a JSON string
rime_update_monitor_response_instance = RimeUpdateMonitorResponse.from_json(json)
# print the JSON string representation of the object
print(RimeUpdateMonitorResponse.to_json())

# convert the object into a dict
rime_update_monitor_response_dict = rime_update_monitor_response_instance.to_dict()
# create an instance of RimeUpdateMonitorResponse from a dict
rime_update_monitor_response_from_dict = RimeUpdateMonitorResponse.from_dict(rime_update_monitor_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

