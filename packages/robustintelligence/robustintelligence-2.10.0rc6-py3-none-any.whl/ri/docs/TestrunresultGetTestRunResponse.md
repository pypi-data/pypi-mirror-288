# TestrunresultGetTestRunResponse

GetTestRunResponse returns the results of a test run.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run** | [**TestrunresultTestRunDetail**](TestrunresultTestRunDetail.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_get_test_run_response import TestrunresultGetTestRunResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultGetTestRunResponse from a JSON string
testrunresult_get_test_run_response_instance = TestrunresultGetTestRunResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultGetTestRunResponse.to_json())

# convert the object into a dict
testrunresult_get_test_run_response_dict = testrunresult_get_test_run_response_instance.to_dict()
# create an instance of TestrunresultGetTestRunResponse from a dict
testrunresult_get_test_run_response_from_dict = TestrunresultGetTestRunResponse.from_dict(testrunresult_get_test_run_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

