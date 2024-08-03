# ProjectListProjectsResponse

ListProjectsResponse returns a list of Projects as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projects** | [**List[ProjectProjectWithDetails]**](ProjectProjectWithDetails.md) |  | [optional] 
**next_page_token** | **str** | A token representing the next page from the list returned by a ListProjects query. | [optional] 
**has_more** | **bool** | A Boolean that specifies whether there are more Projects to return. | [optional] 

## Example

```python
from ri.apiclient.models.project_list_projects_response import ProjectListProjectsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectListProjectsResponse from a JSON string
project_list_projects_response_instance = ProjectListProjectsResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectListProjectsResponse.to_json())

# convert the object into a dict
project_list_projects_response_dict = project_list_projects_response_instance.to_dict()
# create an instance of ProjectListProjectsResponse from a dict
project_list_projects_response_from_dict = ProjectListProjectsResponse.from_dict(project_list_projects_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

