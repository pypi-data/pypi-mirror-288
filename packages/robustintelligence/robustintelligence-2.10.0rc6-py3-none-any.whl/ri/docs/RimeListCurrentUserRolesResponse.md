# RimeListCurrentUserRolesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**roles** | [**List[RimeUserRole]**](RimeUserRole.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_current_user_roles_response import RimeListCurrentUserRolesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListCurrentUserRolesResponse from a JSON string
rime_list_current_user_roles_response_instance = RimeListCurrentUserRolesResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListCurrentUserRolesResponse.to_json())

# convert the object into a dict
rime_list_current_user_roles_response_dict = rime_list_current_user_roles_response_instance.to_dict()
# create an instance of RimeListCurrentUserRolesResponse from a dict
rime_list_current_user_roles_response_from_dict = RimeListCurrentUserRolesResponse.from_dict(rime_list_current_user_roles_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

