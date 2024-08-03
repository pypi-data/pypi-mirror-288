# TestrunresultTestBatchResult

TestBatchResult returns the test batch results. Similar to results_upload.proto but with separation of uploading and querying.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run_id** | **str** | Uniquely specifies a parent Test Run. | [optional] 
**test_type** | **str** |  | [optional] 
**test_name** | **str** | The display-friendly name; for example: &#39;Categorical Feature Drift&#39;. | [optional] 
**description** | **str** | The description of the test. Note: this is currently identical to the display.description_html field. | [optional] 
**test_category** | [**TestrunTestCategoryType**](TestrunTestCategoryType.md) |  | [optional] 
**category** | **str** | The string field &#x60;category&#x60; is deprecated in v2.1 and will be removed in v2.3. Please use the enum field test_category instead, which provides the same info. | [optional] 
**duration_in_millis** | **str** | The duration of the test run. | [optional] 
**severity** | [**RimeSeverity**](RimeSeverity.md) |  | [optional] 
**summary_counts** | [**TestrunresultResultSummaryCounts**](TestrunresultResultSummaryCounts.md) |  | [optional] 
**failing_features** | **List[str]** | The list of failing features. | [optional] 
**metrics** | [**List[RimeTestMetric]**](RimeTestMetric.md) |  | [optional] 
**show_in_test_comparisons** | **bool** | A Boolean that specifies whether to include the test batch in the test comparison page in the web UI. This field is no longer used, and will be removed in 2.3. | [optional] 
**display** | [**TestrunresultTestBatchResultDisplay**](TestrunresultTestBatchResultDisplay.md) |  | [optional] 
**failing_rows_result** | [**RimeFailingRowsResult**](RimeFailingRowsResult.md) |  | [optional] 
**security_test_details** | [**DetectionSecurityEventDetails**](DetectionSecurityEventDetails.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_test_batch_result import TestrunresultTestBatchResult

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultTestBatchResult from a JSON string
testrunresult_test_batch_result_instance = TestrunresultTestBatchResult.from_json(json)
# print the JSON string representation of the object
print(TestrunresultTestBatchResult.to_json())

# convert the object into a dict
testrunresult_test_batch_result_dict = testrunresult_test_batch_result_instance.to_dict()
# create an instance of TestrunresultTestBatchResult from a dict
testrunresult_test_batch_result_from_dict = TestrunresultTestBatchResult.from_dict(testrunresult_test_batch_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

