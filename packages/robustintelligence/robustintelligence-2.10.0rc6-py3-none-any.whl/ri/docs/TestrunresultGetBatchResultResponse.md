# TestrunresultGetBatchResultResponse

GetBatchResultResponse returns the batch result for a test run as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_batch** | [**TestrunresultTestBatchResult**](TestrunresultTestBatchResult.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_get_batch_result_response import TestrunresultGetBatchResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultGetBatchResultResponse from a JSON string
testrunresult_get_batch_result_response_instance = TestrunresultGetBatchResultResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultGetBatchResultResponse.to_json())

# convert the object into a dict
testrunresult_get_batch_result_response_dict = testrunresult_get_batch_result_response_instance.to_dict()
# create an instance of TestrunresultGetBatchResultResponse from a dict
testrunresult_get_batch_result_response_from_dict = TestrunresultGetBatchResultResponse.from_dict(testrunresult_get_batch_result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

