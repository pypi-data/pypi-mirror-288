# ProjectUpdateProjectResponse

UpdateProjectResponse returns an updated Project.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | [**ProjectProject**](ProjectProject.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.project_update_project_response import ProjectUpdateProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectUpdateProjectResponse from a JSON string
project_update_project_response_instance = ProjectUpdateProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectUpdateProjectResponse.to_json())

# convert the object into a dict
project_update_project_response_dict = project_update_project_response_instance.to_dict()
# create an instance of ProjectUpdateProjectResponse from a dict
project_update_project_response_from_dict = ProjectUpdateProjectResponse.from_dict(project_update_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

