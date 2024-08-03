# UserFavoriteProjects

Up to 3 favorite project_ids for each workspace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**project_ids** | [**List[RimeUUID]**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.user_favorite_projects import UserFavoriteProjects

# TODO update the JSON string below
json = "{}"
# create an instance of UserFavoriteProjects from a JSON string
user_favorite_projects_instance = UserFavoriteProjects.from_json(json)
# print the JSON string representation of the object
print(UserFavoriteProjects.to_json())

# convert the object into a dict
user_favorite_projects_dict = user_favorite_projects_instance.to_dict()
# create an instance of UserFavoriteProjects from a dict
user_favorite_projects_from_dict = UserFavoriteProjects.from_dict(user_favorite_projects_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

