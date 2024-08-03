# TestrunresultTestFeatureResult

TestFeatureResult returns the feature results for a given test. Similar to results_upload.proto but with separation of uploading and querying.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url_safe_feature_id** | **str** | The URL-compatible (base 64) encoding of feature name. | [optional] 
**feature_name** | **str** | The human-readable feature name. | [optional] 
**feature_type** | [**RimeFeatureType**](RimeFeatureType.md) |  | [optional] 
**severity** | [**RimeSeverity**](RimeSeverity.md) |  | [optional] 
**summary_counts** | [**TestrunresultResultSummaryCounts**](TestrunresultResultSummaryCounts.md) |  | [optional] 
**failing_tests** | **List[str]** | The list of tests that fail for the feature. | [optional] 
**num_failing_rows** | **str** | The number of rows that fail. | [optional] 
**failing_rows_html** | **str** | The names of the rows that fail; may contain HTML. | [optional] 
**drift_statistic** | [**RimeNamedDouble**](RimeNamedDouble.md) |  | [optional] 
**model_impact** | [**RimeNamedDouble**](RimeNamedDouble.md) |  | [optional] 
**feature_infos** | **List[str]** | The list of feature information used. | [optional] 
**display** | [**TestrunresultTestFeatureResultDisplay**](TestrunresultTestFeatureResultDisplay.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_test_feature_result import TestrunresultTestFeatureResult

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultTestFeatureResult from a JSON string
testrunresult_test_feature_result_instance = TestrunresultTestFeatureResult.from_json(json)
# print the JSON string representation of the object
print(TestrunresultTestFeatureResult.to_json())

# convert the object into a dict
testrunresult_test_feature_result_dict = testrunresult_test_feature_result_instance.to_dict()
# create an instance of TestrunresultTestFeatureResult from a dict
testrunresult_test_feature_result_from_dict = TestrunresultTestFeatureResult.from_dict(testrunresult_test_feature_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

