# TestrunresultListBatchResultsResponse

ListBatchResultsResponse returns all the batch results as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_batches** | [**List[TestrunresultTestBatchResult]**](TestrunresultTestBatchResult.md) | The list of test batch results. | [optional] 
**next_page_token** | **str** | A token representing the next page from the list returned by a ListBatchResults query. | [optional] 
**has_more** | **bool** | A Boolean that specifies whether there are more batch results to return. | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_list_batch_results_response import TestrunresultListBatchResultsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultListBatchResultsResponse from a JSON string
testrunresult_list_batch_results_response_instance = TestrunresultListBatchResultsResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultListBatchResultsResponse.to_json())

# convert the object into a dict
testrunresult_list_batch_results_response_dict = testrunresult_list_batch_results_response_instance.to_dict()
# create an instance of TestrunresultListBatchResultsResponse from a dict
testrunresult_list_batch_results_response_from_dict = TestrunresultListBatchResultsResponse.from_dict(testrunresult_list_batch_results_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

