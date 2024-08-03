# CreateCustomMonitorRequest

CreateCustomMonitorRequest defines the request to create a custom monitor.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**artifact_identifier** | [**MonitorArtifactIdentifier**](MonitorArtifactIdentifier.md) |  | [optional] 
**aggregation** | [**MonitorAggregation**](MonitorAggregation.md) |  | [optional] 
**transform** | [**MonitorTransform**](MonitorTransform.md) |  | [optional] 
**threshold** | [**MonitorThreshold**](MonitorThreshold.md) |  | [optional] 
**notify** | **bool** | Whether to notify when the monitor is triggered. | [optional] 

## Example

```python
from ri.apiclient.models.create_custom_monitor_request import CreateCustomMonitorRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCustomMonitorRequest from a JSON string
create_custom_monitor_request_instance = CreateCustomMonitorRequest.from_json(json)
# print the JSON string representation of the object
print(CreateCustomMonitorRequest.to_json())

# convert the object into a dict
create_custom_monitor_request_dict = create_custom_monitor_request_instance.to_dict()
# create an instance of CreateCustomMonitorRequest from a dict
create_custom_monitor_request_from_dict = CreateCustomMonitorRequest.from_dict(create_custom_monitor_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

