# RimeGetTimeSeriesResponse

GetTimeSeriesResponse returns the results for a time series data. The API currently use message from monitor results, like Threshold and MonitorDataPoint, it may change in the future.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**time_series_name** | **str** | The name of the time series. | [optional] 
**y_axis_label** | **str** |  | [optional] 
**threshold** | [**MonitorThreshold**](MonitorThreshold.md) |  | [optional] 
**data_points** | [**List[RimeMonitorDataPoint]**](RimeMonitorDataPoint.md) | The monitor data points. | [optional] 
**description_html** | **str** | Description of the time series that may contain HTML. | [optional] 
**long_description_tabs** | [**List[RimeLongDescriptionTab]**](RimeLongDescriptionTab.md) | More detailed information about the time series. | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_time_series_response import RimeGetTimeSeriesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetTimeSeriesResponse from a JSON string
rime_get_time_series_response_instance = RimeGetTimeSeriesResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetTimeSeriesResponse.to_json())

# convert the object into a dict
rime_get_time_series_response_dict = rime_get_time_series_response_instance.to_dict()
# create an instance of RimeGetTimeSeriesResponse from a dict
rime_get_time_series_response_from_dict = RimeGetTimeSeriesResponse.from_dict(rime_get_time_series_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

