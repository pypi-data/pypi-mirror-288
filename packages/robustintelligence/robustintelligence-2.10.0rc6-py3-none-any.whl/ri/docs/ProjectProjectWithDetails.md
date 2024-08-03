# ProjectProjectWithDetails

ProjectWithDetails returns the Project and the Project Owner's details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project** | [**ProjectProject**](ProjectProject.md) |  | [optional] 
**owner_details** | [**ProjectOwnerDetails**](ProjectOwnerDetails.md) |  | [optional] 
**last_updated_time** | **datetime** |  | [optional] 

## Example

```python
from ri.apiclient.models.project_project_with_details import ProjectProjectWithDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectProjectWithDetails from a JSON string
project_project_with_details_instance = ProjectProjectWithDetails.from_json(json)
# print the JSON string representation of the object
print(ProjectProjectWithDetails.to_json())

# convert the object into a dict
project_project_with_details_dict = project_project_with_details_instance.to_dict()
# create an instance of ProjectProjectWithDetails from a dict
project_project_with_details_from_dict = ProjectProjectWithDetails.from_dict(project_project_with_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

