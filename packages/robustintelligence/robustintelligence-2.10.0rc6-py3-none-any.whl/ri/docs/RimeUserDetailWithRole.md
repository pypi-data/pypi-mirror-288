# RimeUserDetailWithRole

Specifies a User object and a corresponding Role.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_detail** | [**UserUserDetail**](UserUserDetail.md) |  | [optional] 
**user_role** | [**RimeActorRole**](RimeActorRole.md) |  | [optional] 
**implicit_grant** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_user_detail_with_role import RimeUserDetailWithRole

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUserDetailWithRole from a JSON string
rime_user_detail_with_role_instance = RimeUserDetailWithRole.from_json(json)
# print the JSON string representation of the object
print(RimeUserDetailWithRole.to_json())

# convert the object into a dict
rime_user_detail_with_role_dict = rime_user_detail_with_role_instance.to_dict()
# create an instance of RimeUserDetailWithRole from a dict
rime_user_detail_with_role_from_dict = RimeUserDetailWithRole.from_dict(rime_user_detail_with_role_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

