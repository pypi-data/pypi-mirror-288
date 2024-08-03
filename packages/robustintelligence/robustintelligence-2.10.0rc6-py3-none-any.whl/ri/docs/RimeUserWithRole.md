# RimeUserWithRole

Specifies a User ID and a corresponding Role.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**user_role** | [**RimeActorRole**](RimeActorRole.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_user_with_role import RimeUserWithRole

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUserWithRole from a JSON string
rime_user_with_role_instance = RimeUserWithRole.from_json(json)
# print the JSON string representation of the object
print(RimeUserWithRole.to_json())

# convert the object into a dict
rime_user_with_role_dict = rime_user_with_role_instance.to_dict()
# create an instance of RimeUserWithRole from a dict
rime_user_with_role_from_dict = RimeUserWithRole.from_dict(rime_user_with_role_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

