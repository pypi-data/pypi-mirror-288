# ProjectProject

Project collects test runs for a Stress Test or Continuous Test that relate to a shared machine learning task. Each model for the task is tested by an individual test run. A Continuous Test monitors a currently promoted model over time by continuously testing that model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**use_case** | **str** |  | [optional] 
**ethical_consideration** | **str** |  | [optional] 
**creation_time** | **datetime** |  | [optional] 
**owner_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_task** | [**RimeModelTask**](RimeModelTask.md) |  | [optional] 
**tags** | **List[str]** | List of tags associated with the Project to help organizing Projects. | [optional] 
**firewall_ids** | [**List[RimeUUID]**](RimeUUID.md) | List of Firewall IDs that belong to the Project. | [optional] 
**project_test_suite_config** | [**TestrunTestSuiteConfig**](TestrunTestSuiteConfig.md) |  | [optional] 
**profiling_config** | [**TestrunProfilingConfig**](TestrunProfilingConfig.md) |  | [optional] 
**run_time_info** | [**RuntimeinfoRunTimeInfo**](RuntimeinfoRunTimeInfo.md) |  | [optional] 
**is_published** | **bool** | Published projects are shown on the Workspace overview page. | [optional] 
**last_test_run_time** | **datetime** | Last time a Test Run was successfully uploaded to the Project. | [optional] 
**stress_test_categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) | List of test categories to be run in Stress Testing. | [optional] 
**continuous_test_categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) | List of test categories to be run in Continuous Testing. | [optional] 
**risk_scores** | [**List[RiskscoreRiskScore]**](RiskscoreRiskScore.md) |  | [optional] 
**active_schedule** | [**ProjectScheduleInfo**](ProjectScheduleInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.project_project import ProjectProject

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectProject from a JSON string
project_project_instance = ProjectProject.from_json(json)
# print the JSON string representation of the object
print(ProjectProject.to_json())

# convert the object into a dict
project_project_dict = project_project_instance.to_dict()
# create an instance of ProjectProject from a dict
project_project_from_dict = ProjectProject.from_dict(project_project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

