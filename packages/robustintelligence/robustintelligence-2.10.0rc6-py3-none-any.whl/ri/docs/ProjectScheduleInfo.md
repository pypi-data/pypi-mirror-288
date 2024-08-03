# ProjectScheduleInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schedule_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**activated_time** | **datetime** |  | 

## Example

```python
from ri.apiclient.models.project_schedule_info import ProjectScheduleInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectScheduleInfo from a JSON string
project_schedule_info_instance = ProjectScheduleInfo.from_json(json)
# print the JSON string representation of the object
print(ProjectScheduleInfo.to_json())

# convert the object into a dict
project_schedule_info_dict = project_schedule_info_instance.to_dict()
# create an instance of ProjectScheduleInfo from a dict
project_schedule_info_from_dict = ProjectScheduleInfo.from_dict(project_schedule_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

