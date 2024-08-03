# RimeGetScheduleResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schedule** | [**ScheduleSchedule**](ScheduleSchedule.md) |  | [optional] 
**next_run_time** | **datetime** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_schedule_response import RimeGetScheduleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetScheduleResponse from a JSON string
rime_get_schedule_response_instance = RimeGetScheduleResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetScheduleResponse.to_json())

# convert the object into a dict
rime_get_schedule_response_dict = rime_get_schedule_response_instance.to_dict()
# create an instance of RimeGetScheduleResponse from a dict
rime_get_schedule_response_from_dict = RimeGetScheduleResponse.from_dict(rime_get_schedule_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

