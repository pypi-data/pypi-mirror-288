# UserUserDetail

Information about a user in RIME.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**name** | **str** | Name of the user. | [optional] 
**role** | [**UserRole**](UserRole.md) |  | [optional] 
**email** | **str** |  | [optional] 
**full_name** | **str** |  | [optional] 
**show_tutorial** | **bool** |  | [optional] 
**org_role** | [**RimeActorRole**](RimeActorRole.md) |  | [optional] 
**private_info** | [**UserPrivateInfo**](UserPrivateInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.user_user_detail import UserUserDetail

# TODO update the JSON string below
json = "{}"
# create an instance of UserUserDetail from a JSON string
user_user_detail_instance = UserUserDetail.from_json(json)
# print the JSON string representation of the object
print(UserUserDetail.to_json())

# convert the object into a dict
user_user_detail_dict = user_user_detail_instance.to_dict()
# create an instance of UserUserDetail from a dict
user_user_detail_from_dict = UserUserDetail.from_dict(user_user_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

