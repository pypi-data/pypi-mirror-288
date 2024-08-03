# RimeCreateScheduleRequest

CreateScheduleRequest is the request message for CreateSchedule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**test_run_config** | [**TestrunTestRunConfig**](TestrunTestRunConfig.md) |  | [optional] 
**frequency_cron_expr** | **str** | Cron expression used to determine how often to run the schedule. | 

## Example

```python
from ri.apiclient.models.rime_create_schedule_request import RimeCreateScheduleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateScheduleRequest from a JSON string
rime_create_schedule_request_instance = RimeCreateScheduleRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateScheduleRequest.to_json())

# convert the object into a dict
rime_create_schedule_request_dict = rime_create_schedule_request_instance.to_dict()
# create an instance of RimeCreateScheduleRequest from a dict
rime_create_schedule_request_from_dict = RimeCreateScheduleRequest.from_dict(rime_create_schedule_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

