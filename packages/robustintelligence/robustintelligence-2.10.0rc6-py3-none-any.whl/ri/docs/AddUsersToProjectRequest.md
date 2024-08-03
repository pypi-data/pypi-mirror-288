# AddUsersToProjectRequest

AddUsersToProjectRequest defines a request to add user new permissions to the Project.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **object** | Uniquely specifies a Project. | [optional] 
**users** | [**List[RimeUserWithRole]**](RimeUserWithRole.md) | Pairs of users and their roles for the Project. | [optional] 

## Example

```python
from ri.apiclient.models.add_users_to_project_request import AddUsersToProjectRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddUsersToProjectRequest from a JSON string
add_users_to_project_request_instance = AddUsersToProjectRequest.from_json(json)
# print the JSON string representation of the object
print(AddUsersToProjectRequest.to_json())

# convert the object into a dict
add_users_to_project_request_dict = add_users_to_project_request_instance.to_dict()
# create an instance of AddUsersToProjectRequest from a dict
add_users_to_project_request_from_dict = AddUsersToProjectRequest.from_dict(add_users_to_project_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

