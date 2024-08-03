# UpdateMonitorRequest

UpdateMonitorRequest defines the request to update a monitor.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**monitor** | [**UpdateMonitorRequestMonitor**](UpdateMonitorRequestMonitor.md) |  | [optional] 
**mask** | **str** | The field mask. | [optional] 

## Example

```python
from ri.apiclient.models.update_monitor_request import UpdateMonitorRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateMonitorRequest from a JSON string
update_monitor_request_instance = UpdateMonitorRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateMonitorRequest.to_json())

# convert the object into a dict
update_monitor_request_dict = update_monitor_request_instance.to_dict()
# create an instance of UpdateMonitorRequest from a dict
update_monitor_request_from_dict = UpdateMonitorRequest.from_dict(update_monitor_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

