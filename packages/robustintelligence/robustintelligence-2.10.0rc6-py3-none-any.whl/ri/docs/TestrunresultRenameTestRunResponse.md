# TestrunresultRenameTestRunResponse

RenameTestRunResponse returns the renamed test run as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run** | [**TestrunresultTestRunDetail**](TestrunresultTestRunDetail.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_rename_test_run_response import TestrunresultRenameTestRunResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultRenameTestRunResponse from a JSON string
testrunresult_rename_test_run_response_instance = TestrunresultRenameTestRunResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultRenameTestRunResponse.to_json())

# convert the object into a dict
testrunresult_rename_test_run_response_dict = testrunresult_rename_test_run_response_instance.to_dict()
# create an instance of TestrunresultRenameTestRunResponse from a dict
testrunresult_rename_test_run_response_from_dict = TestrunresultRenameTestRunResponse.from_dict(testrunresult_rename_test_run_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

