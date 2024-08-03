# ProjectListUsersOfProjectResponse

ListUsersOfProjectResponse returns a list of users of the Project as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**users** | [**List[RimeUserDetailWithRole]**](RimeUserDetailWithRole.md) |  | [optional] 
**next_page_token** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.project_list_users_of_project_response import ProjectListUsersOfProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectListUsersOfProjectResponse from a JSON string
project_list_users_of_project_response_instance = ProjectListUsersOfProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectListUsersOfProjectResponse.to_json())

# convert the object into a dict
project_list_users_of_project_response_dict = project_list_users_of_project_response_instance.to_dict()
# create an instance of ProjectListUsersOfProjectResponse from a dict
project_list_users_of_project_response_from_dict = ProjectListUsersOfProjectResponse.from_dict(project_list_users_of_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

