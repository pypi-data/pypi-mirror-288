# TestrunresultListTestRunsResponse

ListTestRunsResponse returns all the test runs as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_runs** | [**List[TestrunresultTestRunDetail]**](TestrunresultTestRunDetail.md) | The details of the test runs. | [optional] 
**next_page_token** | **str** | A token representing the next page from the list returned by a ListTestRuns query. | [optional] 
**has_more** | **bool** | A Boolean that specifies whether there are more test runs to return. | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_list_test_runs_response import TestrunresultListTestRunsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultListTestRunsResponse from a JSON string
testrunresult_list_test_runs_response_instance = TestrunresultListTestRunsResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultListTestRunsResponse.to_json())

# convert the object into a dict
testrunresult_list_test_runs_response_dict = testrunresult_list_test_runs_response_instance.to_dict()
# create an instance of TestrunresultListTestRunsResponse from a dict
testrunresult_list_test_runs_response_from_dict = TestrunresultListTestRunsResponse.from_dict(testrunresult_list_test_runs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

