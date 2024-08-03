# ProjectListProjectsRequestQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_published** | **bool** | Optional: If true, return published projects. If false, return unpublished projects. If not specified, return all projects. | [optional] 
**creation_time_range** | [**RimeTimeInterval**](RimeTimeInterval.md) |  | [optional] 
**last_test_run_time_range** | [**RimeTimeInterval**](RimeTimeInterval.md) |  | [optional] 
**stress_test_categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) | Optional: When specified, return all projects whose ST categories are a superset of the ST categories provided here. | [optional] 
**continuous_test_categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) | Optional: When specified, return all projects whose CT categories are a superset of the CT categories provided here. | [optional] 
**owner_email** | **str** | Optional: When specified, return all projects whose owner email matches. | [optional] 
**model_tasks** | [**List[RimeModelTask]**](RimeModelTask.md) | Optional: When specified, return all projects whose model task is the provided model task. | [optional] 
**status** | [**ProjectProjectStatus**](ProjectProjectStatus.md) |  | [optional] 
**sort** | [**RimeSortSpec**](RimeSortSpec.md) |  | [optional] 
**search** | [**RimeSearchSpec**](RimeSearchSpec.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.project_list_projects_request_query import ProjectListProjectsRequestQuery

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectListProjectsRequestQuery from a JSON string
project_list_projects_request_query_instance = ProjectListProjectsRequestQuery.from_json(json)
# print the JSON string representation of the object
print(ProjectListProjectsRequestQuery.to_json())

# convert the object into a dict
project_list_projects_request_query_dict = project_list_projects_request_query_instance.to_dict()
# create an instance of ProjectListProjectsRequestQuery from a dict
project_list_projects_request_query_from_dict = ProjectListProjectsRequestQuery.from_dict(project_list_projects_request_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

