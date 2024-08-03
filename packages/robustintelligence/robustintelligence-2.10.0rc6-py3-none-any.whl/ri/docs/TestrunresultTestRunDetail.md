# TestrunresultTestRunDetail

TestRunDetail returns the details for a given test run.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run_id** | **str** | Uniquely specifies a Test Run. | [optional] 
**name** | **str** | The name of the Test Run. | [optional] 
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**testing_type** | [**RimeTestType**](RimeTestType.md) |  | [optional] 
**model_task** | [**RimeModelTask**](RimeModelTask.md) |  | [optional] 
**ref_data_id** | **str** | Uniquely specifies a reference dataset. | [optional] 
**eval_data_id** | **str** | Uniquely specifies an evaluation dataset. | [optional] 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**upload_time** | **datetime** | The upload time of the test run. | [optional] 
**web_app_url** | [**RimeSafeURL**](RimeSafeURL.md) |  | [optional] 
**test_categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) | The list of child references to the category tests belonging to this test run. | [optional] 
**metrics** | [**TestrunresultTestRunMetrics**](TestrunresultTestRunMetrics.md) |  | [optional] 
**status** | [**RimeTestTaskStatus**](RimeTestTaskStatus.md) |  | [optional] 
**progress** | **str** | Human-readable succinct message about the progress of the test run. | [optional] 
**rime_version** | **str** | The version of Robust Intelligence that ran this test. | [optional] 
**bin_time_interval** | [**RimeTimeInterval**](RimeTimeInterval.md) |  | [optional] 
**ref_data_sampling_pct** | **float** | Percentage of the reference dataset used for this test. If no sampling occurred, this will be 1.0. | [optional] 
**eval_data_sampling_pct** | **float** | Percentage of the evaluation dataset used for this test. If no sampling occurred, this will be 1.0. | [optional] 
**schedule_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_test_run_detail import TestrunresultTestRunDetail

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultTestRunDetail from a JSON string
testrunresult_test_run_detail_instance = TestrunresultTestRunDetail.from_json(json)
# print the JSON string representation of the object
print(TestrunresultTestRunDetail.to_json())

# convert the object into a dict
testrunresult_test_run_detail_dict = testrunresult_test_run_detail_instance.to_dict()
# create an instance of TestrunresultTestRunDetail from a dict
testrunresult_test_run_detail_from_dict = TestrunresultTestRunDetail.from_dict(testrunresult_test_run_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

