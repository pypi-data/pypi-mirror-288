# RimeCategoryTestResult

CategoryTestResult is a summary of a single category of tests in Robust Intelligence. For instance, the \"Drift\" category includes specific tests such as Prediction Drift or Label Drift. The CategoryTestResult for Drift includes an overall severity and other details aggregated across those individual tests.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | When combined with the test run ID, this uniquely identifies a category test result. | [optional] 
**severity** | [**RimeSeverity**](RimeSeverity.md) |  | [optional] 
**suggestion** | [**RimeSuggestion**](RimeSuggestion.md) |  | [optional] 
**category_metrics** | [**List[RimeCategoryMetric]**](RimeCategoryMetric.md) | Category metrics are aggregated or important metrics for the category. | [optional] 
**test_batch_types** | **List[str]** | List of the tests in the category. | [optional] 
**description** | **str** | Human-readable description of the category test result. | [optional] 
**severity_counts** | [**RimeSeverityCounts**](RimeSeverityCounts.md) |  | [optional] 
**failing_test_types** | **List[str]** | List of all the failing test types. | [optional] 
**duration** | **float** | Duration is the total time in seconds for tests in that category. | [optional] 
**category_importance** | **float** | The relative importance of the category. | [optional] 
**risk_category** | [**RiskscoreRiskCategoryType**](RiskscoreRiskCategoryType.md) |  | [optional] 
**test_category** | [**TestrunTestCategoryType**](TestrunTestCategoryType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_category_test_result import RimeCategoryTestResult

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCategoryTestResult from a JSON string
rime_category_test_result_instance = RimeCategoryTestResult.from_json(json)
# print the JSON string representation of the object
print(RimeCategoryTestResult.to_json())

# convert the object into a dict
rime_category_test_result_dict = rime_category_test_result_instance.to_dict()
# create an instance of RimeCategoryTestResult from a dict
rime_category_test_result_from_dict = RimeCategoryTestResult.from_dict(rime_category_test_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

