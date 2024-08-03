# TestrunresultTestCase

TestCase returns information for a given test case.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run_id** | **str** | Uniquely specifies a Test Run. | [optional] 
**features** | **List[str]** | The list of features used in the test case. | [optional] 
**test_batch_type** | **str** | The type of test batch. | [optional] 
**status** | [**RimeTestCaseStatus**](RimeTestCaseStatus.md) |  | [optional] 
**severity** | [**RimeSeverity**](RimeSeverity.md) |  | [optional] 
**importance_score** | **float** | The model impact of the test case. | [optional] 
**test_category** | [**TestrunTestCategoryType**](TestrunTestCategoryType.md) |  | [optional] 
**category** | **str** | The string field &#x60;category&#x60; is deprecated in v2.1 and will be removed in v2.3. Please use the enum field test_category instead, which provides the same info. | [optional] 
**metrics** | [**List[RimeTestMetric]**](RimeTestMetric.md) |  | [optional] 
**url_safe_feature_id** | **str** | Optional URL-safe feature ID if the test case is associated with a feature. This may be empty for modalities that do not have features or test cases that pertain to two or more features, such as subset tests. | [optional] 
**test_case_id** | **str** | Together with the Test Run ID and the test batch type, this forms the primary key for the test case. | [optional] 
**display** | [**TestrunresultTestCaseDisplay**](TestrunresultTestCaseDisplay.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_test_case import TestrunresultTestCase

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultTestCase from a JSON string
testrunresult_test_case_instance = TestrunresultTestCase.from_json(json)
# print the JSON string representation of the object
print(TestrunresultTestCase.to_json())

# convert the object into a dict
testrunresult_test_case_dict = testrunresult_test_case_instance.to_dict()
# create an instance of TestrunresultTestCase from a dict
testrunresult_test_case_from_dict = TestrunresultTestCase.from_dict(testrunresult_test_case_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

