# UpdateUserRequestUser

Information about a user in RIME.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **object** | Unique ID of an object in RIME. | [optional] 
**name** | **str** | Name of the user. | [optional] 
**role** | [**UserRole**](UserRole.md) |  | [optional] 
**email** | **str** |  | [optional] 
**full_name** | **str** |  | [optional] 
**show_tutorial** | **bool** |  | [optional] 
**org_role** | [**RimeActorRole**](RimeActorRole.md) |  | [optional] 
**private_info** | [**UserPrivateInfo**](UserPrivateInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.update_user_request_user import UpdateUserRequestUser

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserRequestUser from a JSON string
update_user_request_user_instance = UpdateUserRequestUser.from_json(json)
# print the JSON string representation of the object
print(UpdateUserRequestUser.to_json())

# convert the object into a dict
update_user_request_user_dict = update_user_request_user_instance.to_dict()
# create an instance of UpdateUserRequestUser from a dict
update_user_request_user_from_dict = UpdateUserRequestUser.from_dict(update_user_request_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

