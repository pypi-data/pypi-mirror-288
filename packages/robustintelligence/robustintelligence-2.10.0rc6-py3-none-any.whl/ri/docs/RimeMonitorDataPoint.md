# RimeMonitorDataPoint

MonitorDataPoint defines a single data point in the monitor time series. It identifies both a metric value and time interval.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time_interval** | [**RimeTimeInterval**](RimeTimeInterval.md) |  | [optional] 
**monitor_value** | **float** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_monitor_data_point import RimeMonitorDataPoint

# TODO update the JSON string below
json = "{}"
# create an instance of RimeMonitorDataPoint from a JSON string
rime_monitor_data_point_instance = RimeMonitorDataPoint.from_json(json)
# print the JSON string representation of the object
print(RimeMonitorDataPoint.to_json())

# convert the object into a dict
rime_monitor_data_point_dict = rime_monitor_data_point_instance.to_dict()
# create an instance of RimeMonitorDataPoint from a dict
rime_monitor_data_point_from_dict = RimeMonitorDataPoint.from_dict(rime_monitor_data_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

