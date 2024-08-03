# RimeUpdateScheduleResponse

UpdateScheduleResponse is the response message for UpdateSchedule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schedule** | [**ScheduleSchedule**](ScheduleSchedule.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_update_schedule_response import RimeUpdateScheduleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUpdateScheduleResponse from a JSON string
rime_update_schedule_response_instance = RimeUpdateScheduleResponse.from_json(json)
# print the JSON string representation of the object
print(RimeUpdateScheduleResponse.to_json())

# convert the object into a dict
rime_update_schedule_response_dict = rime_update_schedule_response_instance.to_dict()
# create an instance of RimeUpdateScheduleResponse from a dict
rime_update_schedule_response_from_dict = RimeUpdateScheduleResponse.from_dict(rime_update_schedule_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

