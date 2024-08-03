# ProjectActivateScheduleForProjectResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**active_schedule** | [**ProjectScheduleInfo**](ProjectScheduleInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.project_activate_schedule_for_project_response import ProjectActivateScheduleForProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectActivateScheduleForProjectResponse from a JSON string
project_activate_schedule_for_project_response_instance = ProjectActivateScheduleForProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectActivateScheduleForProjectResponse.to_json())

# convert the object into a dict
project_activate_schedule_for_project_response_dict = project_activate_schedule_for_project_response_instance.to_dict()
# create an instance of ProjectActivateScheduleForProjectResponse from a dict
project_activate_schedule_for_project_response_from_dict = ProjectActivateScheduleForProjectResponse.from_dict(project_activate_schedule_for_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

