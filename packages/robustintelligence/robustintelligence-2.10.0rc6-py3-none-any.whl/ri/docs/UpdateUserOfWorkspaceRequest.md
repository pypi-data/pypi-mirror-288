# UpdateUserOfWorkspaceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **object** | Unique ID of an object in RIME. | [optional] 
**user** | [**UpdateUserOfProjectRequestUser**](UpdateUserOfProjectRequestUser.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.update_user_of_workspace_request import UpdateUserOfWorkspaceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserOfWorkspaceRequest from a JSON string
update_user_of_workspace_request_instance = UpdateUserOfWorkspaceRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateUserOfWorkspaceRequest.to_json())

# convert the object into a dict
update_user_of_workspace_request_dict = update_user_of_workspace_request_instance.to_dict()
# create an instance of UpdateUserOfWorkspaceRequest from a dict
update_user_of_workspace_request_from_dict = UpdateUserOfWorkspaceRequest.from_dict(update_user_of_workspace_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

