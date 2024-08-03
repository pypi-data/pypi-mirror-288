# AddUsersToWorkspaceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **object** | Unique ID of an object in RIME. | [optional] 
**users** | [**List[RimeUserWithRole]**](RimeUserWithRole.md) | List of Users to add to the Workspace. | 

## Example

```python
from ri.apiclient.models.add_users_to_workspace_request import AddUsersToWorkspaceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddUsersToWorkspaceRequest from a JSON string
add_users_to_workspace_request_instance = AddUsersToWorkspaceRequest.from_json(json)
# print the JSON string representation of the object
print(AddUsersToWorkspaceRequest.to_json())

# convert the object into a dict
add_users_to_workspace_request_dict = add_users_to_workspace_request_instance.to_dict()
# create an instance of AddUsersToWorkspaceRequest from a dict
add_users_to_workspace_request_from_dict = AddUsersToWorkspaceRequest.from_dict(add_users_to_workspace_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

