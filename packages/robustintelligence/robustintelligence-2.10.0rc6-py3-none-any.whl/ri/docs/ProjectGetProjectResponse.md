# ProjectGetProjectResponse

GetProjectResponse returns a project with its owner details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | [**ProjectProjectWithDetails**](ProjectProjectWithDetails.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.project_get_project_response import ProjectGetProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectGetProjectResponse from a JSON string
project_get_project_response_instance = ProjectGetProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectGetProjectResponse.to_json())

# convert the object into a dict
project_get_project_response_dict = project_get_project_response_instance.to_dict()
# create an instance of ProjectGetProjectResponse from a dict
project_get_project_response_from_dict = ProjectGetProjectResponse.from_dict(project_get_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

