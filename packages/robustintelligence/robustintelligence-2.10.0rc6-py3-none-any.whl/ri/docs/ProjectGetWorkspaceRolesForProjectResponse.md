# ProjectGetWorkspaceRolesForProjectResponse

GetWorkspaceRolesForProjectResponse returns a list of role pairs of Workspace user roles and their Project user roles.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**role_pairs** | [**List[RimeParentRoleSubjectRolePair]**](RimeParentRoleSubjectRolePair.md) | The elements of role_pairs maps each Workspace role to a Project role. | [optional] 

## Example

```python
from ri.apiclient.models.project_get_workspace_roles_for_project_response import ProjectGetWorkspaceRolesForProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectGetWorkspaceRolesForProjectResponse from a JSON string
project_get_workspace_roles_for_project_response_instance = ProjectGetWorkspaceRolesForProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectGetWorkspaceRolesForProjectResponse.to_json())

# convert the object into a dict
project_get_workspace_roles_for_project_response_dict = project_get_workspace_roles_for_project_response_instance.to_dict()
# create an instance of ProjectGetWorkspaceRolesForProjectResponse from a dict
project_get_workspace_roles_for_project_response_from_dict = ProjectGetWorkspaceRolesForProjectResponse.from_dict(project_get_workspace_roles_for_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

