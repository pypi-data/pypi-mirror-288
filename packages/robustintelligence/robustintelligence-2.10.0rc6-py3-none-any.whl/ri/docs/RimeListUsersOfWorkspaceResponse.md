# RimeListUsersOfWorkspaceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**users** | [**List[RimeUserDetailWithRole]**](RimeUserDetailWithRole.md) |  | [optional] 
**next_page_token** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_users_of_workspace_response import RimeListUsersOfWorkspaceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListUsersOfWorkspaceResponse from a JSON string
rime_list_users_of_workspace_response_instance = RimeListUsersOfWorkspaceResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListUsersOfWorkspaceResponse.to_json())

# convert the object into a dict
rime_list_users_of_workspace_response_dict = rime_list_users_of_workspace_response_instance.to_dict()
# create an instance of RimeListUsersOfWorkspaceResponse from a dict
rime_list_users_of_workspace_response_from_dict = RimeListUsersOfWorkspaceResponse.from_dict(rime_list_users_of_workspace_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

