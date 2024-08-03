# UpdateUserOfProjectRequestUser

Specifies a User ID and a corresponding Role.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **object** | Unique ID of an object in RIME. | [optional] 
**user_role** | [**RimeActorRole**](RimeActorRole.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.update_user_of_project_request_user import UpdateUserOfProjectRequestUser

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserOfProjectRequestUser from a JSON string
update_user_of_project_request_user_instance = UpdateUserOfProjectRequestUser.from_json(json)
# print the JSON string representation of the object
print(UpdateUserOfProjectRequestUser.to_json())

# convert the object into a dict
update_user_of_project_request_user_dict = update_user_of_project_request_user_instance.to_dict()
# create an instance of UpdateUserOfProjectRequestUser from a dict
update_user_of_project_request_user_from_dict = UpdateUserOfProjectRequestUser.from_dict(update_user_of_project_request_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

