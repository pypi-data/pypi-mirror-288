# RimeCreateScheduleResponse

CreateScheduleResponse is the response message for CreateSchedule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schedule_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_schedule_response import RimeCreateScheduleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateScheduleResponse from a JSON string
rime_create_schedule_response_instance = RimeCreateScheduleResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateScheduleResponse.to_json())

# convert the object into a dict
rime_create_schedule_response_dict = rime_create_schedule_response_instance.to_dict()
# create an instance of RimeCreateScheduleResponse from a dict
rime_create_schedule_response_from_dict = RimeCreateScheduleResponse.from_dict(rime_create_schedule_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

