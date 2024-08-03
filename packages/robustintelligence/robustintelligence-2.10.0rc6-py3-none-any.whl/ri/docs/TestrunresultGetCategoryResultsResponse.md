# TestrunresultGetCategoryResultsResponse

GetCategoryResultsResponse returns the list of summary tests as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category_test_results** | [**List[RimeCategoryTestResult]**](RimeCategoryTestResult.md) | The list of summary test results. | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_get_category_results_response import TestrunresultGetCategoryResultsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultGetCategoryResultsResponse from a JSON string
testrunresult_get_category_results_response_instance = TestrunresultGetCategoryResultsResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultGetCategoryResultsResponse.to_json())

# convert the object into a dict
testrunresult_get_category_results_response_dict = testrunresult_get_category_results_response_instance.to_dict()
# create an instance of TestrunresultGetCategoryResultsResponse from a dict
testrunresult_get_category_results_response_from_dict = TestrunresultGetCategoryResultsResponse.from_dict(testrunresult_get_category_results_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

