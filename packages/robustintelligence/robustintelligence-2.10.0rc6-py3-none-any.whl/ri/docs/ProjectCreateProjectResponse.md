# ProjectCreateProjectResponse

CreateProjectResponse returns a newly created Project.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | [**ProjectProject**](ProjectProject.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.project_create_project_response import ProjectCreateProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectCreateProjectResponse from a JSON string
project_create_project_response_instance = ProjectCreateProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectCreateProjectResponse.to_json())

# convert the object into a dict
project_create_project_response_dict = project_create_project_response_instance.to_dict()
# create an instance of ProjectCreateProjectResponse from a dict
project_create_project_response_from_dict = ProjectCreateProjectResponse.from_dict(project_create_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

