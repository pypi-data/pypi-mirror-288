# RimeUserRole

Represents a role to an associated subject i.e. an Admin role to a subject Project.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**subject_type** | [**RimeSubjectType**](RimeSubjectType.md) |  | [optional] 
**subject_id** | **str** |  | [optional] 
**role** | [**RimeActorRole**](RimeActorRole.md) |  | [optional] 
**implicit_grant** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_user_role import RimeUserRole

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUserRole from a JSON string
rime_user_role_instance = RimeUserRole.from_json(json)
# print the JSON string representation of the object
print(RimeUserRole.to_json())

# convert the object into a dict
rime_user_role_dict = rime_user_role_instance.to_dict()
# create an instance of RimeUserRole from a dict
rime_user_role_from_dict = RimeUserRole.from_dict(rime_user_role_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

