# ProjectUpdateWorkspaceRolesForProjectResponse

UpdateWorkspaceRolesForProjectResponse returns an updated list of role pairs of the Workspace user roles and their Project user roles.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**role_pairs** | [**List[RimeParentRoleSubjectRolePair]**](RimeParentRoleSubjectRolePair.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.project_update_workspace_roles_for_project_response import ProjectUpdateWorkspaceRolesForProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectUpdateWorkspaceRolesForProjectResponse from a JSON string
project_update_workspace_roles_for_project_response_instance = ProjectUpdateWorkspaceRolesForProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectUpdateWorkspaceRolesForProjectResponse.to_json())

# convert the object into a dict
project_update_workspace_roles_for_project_response_dict = project_update_workspace_roles_for_project_response_instance.to_dict()
# create an instance of ProjectUpdateWorkspaceRolesForProjectResponse from a dict
project_update_workspace_roles_for_project_response_from_dict = ProjectUpdateWorkspaceRolesForProjectResponse.from_dict(project_update_workspace_roles_for_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

