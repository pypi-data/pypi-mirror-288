# ProjectCreateProjectRequest

CreateProjectRequest defines a request to create a new Project.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 
**use_case** | **str** |  | [optional] 
**ethical_consideration** | **str** |  | [optional] 
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_task** | [**RimeModelTask**](RimeModelTask.md) |  | [optional] 
**tags** | **List[str]** | List of tags associated with the Project to help organizing Projects. | [optional] 
**profiling_config** | [**TestrunProfilingConfig**](TestrunProfilingConfig.md) |  | [optional] 
**is_published** | **bool** | Published projects are shown on the Workspace overview page. | [optional] 
**run_time_info** | [**RuntimeinfoRunTimeInfo**](RuntimeinfoRunTimeInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.project_create_project_request import ProjectCreateProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectCreateProjectRequest from a JSON string
project_create_project_request_instance = ProjectCreateProjectRequest.from_json(json)
# print the JSON string representation of the object
print(ProjectCreateProjectRequest.to_json())

# convert the object into a dict
project_create_project_request_dict = project_create_project_request_instance.to_dict()
# create an instance of ProjectCreateProjectRequest from a dict
project_create_project_request_from_dict = ProjectCreateProjectRequest.from_dict(project_create_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

