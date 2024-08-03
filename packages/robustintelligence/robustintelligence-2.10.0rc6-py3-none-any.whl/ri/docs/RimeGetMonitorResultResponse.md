# RimeGetMonitorResultResponse

GetMonitorResultResponse returns the results for a monitor within a time range.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**monitor_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**monitor_name** | **str** | The name of the monitor. | [optional] 
**metric_name** | **str** |  | [optional] 
**threshold** | [**MonitorThreshold**](MonitorThreshold.md) |  | [optional] 
**data_points** | [**List[RimeMonitorDataPoint]**](RimeMonitorDataPoint.md) | The monitor data points. | [optional] 
**description_html** | **str** | Description of the monitor that may contain HTML. | [optional] 
**long_description_tabs** | [**List[RimeLongDescriptionTab]**](RimeLongDescriptionTab.md) | More detailed information about the monitor. | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_monitor_result_response import RimeGetMonitorResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetMonitorResultResponse from a JSON string
rime_get_monitor_result_response_instance = RimeGetMonitorResultResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetMonitorResultResponse.to_json())

# convert the object into a dict
rime_get_monitor_result_response_dict = rime_get_monitor_result_response_instance.to_dict()
# create an instance of RimeGetMonitorResultResponse from a dict
rime_get_monitor_result_response_from_dict = RimeGetMonitorResultResponse.from_dict(rime_get_monitor_result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

