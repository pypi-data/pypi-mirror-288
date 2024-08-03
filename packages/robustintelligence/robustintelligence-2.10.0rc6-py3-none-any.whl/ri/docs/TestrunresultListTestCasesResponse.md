# TestrunresultListTestCasesResponse

ListTestCasesResponse returns the list of test cases requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_cases** | [**List[TestrunresultTestCase]**](TestrunresultTestCase.md) | The list of test cases. | [optional] 
**next_page_token** | **str** | A token representing the next page from the list returned by a ListTestCases query. | [optional] 
**has_more** | **bool** | A Boolean flag that specifies whether there are more test cases to return. | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_list_test_cases_response import TestrunresultListTestCasesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultListTestCasesResponse from a JSON string
testrunresult_list_test_cases_response_instance = TestrunresultListTestCasesResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultListTestCasesResponse.to_json())

# convert the object into a dict
testrunresult_list_test_cases_response_dict = testrunresult_list_test_cases_response_instance.to_dict()
# create an instance of TestrunresultListTestCasesResponse from a dict
testrunresult_list_test_cases_response_from_dict = TestrunresultListTestCasesResponse.from_dict(testrunresult_list_test_cases_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

