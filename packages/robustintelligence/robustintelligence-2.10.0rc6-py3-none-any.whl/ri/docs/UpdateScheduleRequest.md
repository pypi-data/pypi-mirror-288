# UpdateScheduleRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schedule_id** | **object** | Unique ID of an object in RIME. | [optional] 
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**test_run_config** | [**TestrunTestRunConfig**](TestrunTestRunConfig.md) |  | [optional] 
**frequency_cron_expr** | **str** | Cron expression used to determine how often to run the schedule. Accepts \&quot;@hourly\&quot;, \&quot;@daily\&quot;, \&quot;@weekly\&quot;, and \&quot;@monthly\&quot;. | [optional] 

## Example

```python
from ri.apiclient.models.update_schedule_request import UpdateScheduleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateScheduleRequest from a JSON string
update_schedule_request_instance = UpdateScheduleRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateScheduleRequest.to_json())

# convert the object into a dict
update_schedule_request_dict = update_schedule_request_instance.to_dict()
# create an instance of UpdateScheduleRequest from a dict
update_schedule_request_from_dict = UpdateScheduleRequest.from_dict(update_schedule_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

