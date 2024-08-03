# UpdateWorkspaceRolesForProjectRequest

UpdateWorkspaceRolesForProjectRequest defines a request to set user roles on a Project based on the their roles in the Workspace that contains the Project.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **object** | Uniquely specifies a Project. | [optional] 
**role_pairs** | [**List[RimeParentRoleSubjectRolePair]**](RimeParentRoleSubjectRolePair.md) | The elements of role_pairs maps each Workspace role to a Project role. For example, you can specify that a user with admin rights on a Workspace will get viewer rights on Projects in that Workspace. | 

## Example

```python
from ri.apiclient.models.update_workspace_roles_for_project_request import UpdateWorkspaceRolesForProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateWorkspaceRolesForProjectRequest from a JSON string
update_workspace_roles_for_project_request_instance = UpdateWorkspaceRolesForProjectRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateWorkspaceRolesForProjectRequest.to_json())

# convert the object into a dict
update_workspace_roles_for_project_request_dict = update_workspace_roles_for_project_request_instance.to_dict()
# create an instance of UpdateWorkspaceRolesForProjectRequest from a dict
update_workspace_roles_for_project_request_from_dict = UpdateWorkspaceRolesForProjectRequest.from_dict(update_workspace_roles_for_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

