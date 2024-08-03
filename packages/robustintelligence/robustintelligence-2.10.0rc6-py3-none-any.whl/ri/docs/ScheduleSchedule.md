# ScheduleSchedule


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schedule_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**test_run_config** | [**TestrunTestRunConfig**](TestrunTestRunConfig.md) |  | [optional] 
**frequency_cron_expr** | **str** | Cron expression used to determine how often to run the schedule. Accepts \&quot;@hourly\&quot;, \&quot;@daily\&quot;, \&quot;@weekly\&quot;, and \&quot;@monthly\&quot;. | [optional] 

## Example

```python
from ri.apiclient.models.schedule_schedule import ScheduleSchedule

# TODO update the JSON string below
json = "{}"
# create an instance of ScheduleSchedule from a JSON string
schedule_schedule_instance = ScheduleSchedule.from_json(json)
# print the JSON string representation of the object
print(ScheduleSchedule.to_json())

# convert the object into a dict
schedule_schedule_dict = schedule_schedule_instance.to_dict()
# create an instance of ScheduleSchedule from a dict
schedule_schedule_from_dict = ScheduleSchedule.from_dict(schedule_schedule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

