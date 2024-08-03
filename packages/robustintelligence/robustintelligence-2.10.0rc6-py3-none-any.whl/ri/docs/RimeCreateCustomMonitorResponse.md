# RimeCreateCustomMonitorResponse

CreateCustomMonitorResponse returns the created custom monitor.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**monitor** | [**MonitorMonitor**](MonitorMonitor.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_custom_monitor_response import RimeCreateCustomMonitorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateCustomMonitorResponse from a JSON string
rime_create_custom_monitor_response_instance = RimeCreateCustomMonitorResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateCustomMonitorResponse.to_json())

# convert the object into a dict
rime_create_custom_monitor_response_dict = rime_create_custom_monitor_response_instance.to_dict()
# create an instance of RimeCreateCustomMonitorResponse from a dict
rime_create_custom_monitor_response_from_dict = RimeCreateCustomMonitorResponse.from_dict(rime_create_custom_monitor_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

