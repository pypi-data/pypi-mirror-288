# UserPrivateInfo

PrivateInfo holds fields which are considered private to a user.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**favorite_projects** | [**List[UserFavoriteProjects]**](UserFavoriteProjects.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.user_private_info import UserPrivateInfo

# TODO update the JSON string below
json = "{}"
# create an instance of UserPrivateInfo from a JSON string
user_private_info_instance = UserPrivateInfo.from_json(json)
# print the JSON string representation of the object
print(UserPrivateInfo.to_json())

# convert the object into a dict
user_private_info_dict = user_private_info_instance.to_dict()
# create an instance of UserPrivateInfo from a dict
user_private_info_from_dict = UserPrivateInfo.from_dict(user_private_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

