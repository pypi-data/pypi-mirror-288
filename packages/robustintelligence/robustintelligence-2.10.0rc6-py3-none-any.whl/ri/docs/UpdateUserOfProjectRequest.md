# UpdateUserOfProjectRequest

UpdateUserOfProjectRequest defines a request to update permissions of a user for the Project.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **object** | Uniquely specifies a Project. | [optional] 
**user** | [**UpdateUserOfProjectRequestUser**](UpdateUserOfProjectRequestUser.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.update_user_of_project_request import UpdateUserOfProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserOfProjectRequest from a JSON string
update_user_of_project_request_instance = UpdateUserOfProjectRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateUserOfProjectRequest.to_json())

# convert the object into a dict
update_user_of_project_request_dict = update_user_of_project_request_instance.to_dict()
# create an instance of UpdateUserOfProjectRequest from a dict
update_user_of_project_request_from_dict = UpdateUserOfProjectRequest.from_dict(update_user_of_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

