# ApigenerativevalidationListTestRunsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_runs** | [**List[GenerativevalidationGenerativeValidationTestRun]**](GenerativevalidationGenerativeValidationTestRun.md) | The list of generative testing results. | [optional] 
**next_page_token** | **str** | A token representing the next page from the list returned by a query. | [optional] 
**has_more** | **bool** | A Boolean flag that specifies whether there are more results to return. | [optional] 

## Example

```python
from ri.apiclient.models.apigenerativevalidation_list_test_runs_response import ApigenerativevalidationListTestRunsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ApigenerativevalidationListTestRunsResponse from a JSON string
apigenerativevalidation_list_test_runs_response_instance = ApigenerativevalidationListTestRunsResponse.from_json(json)
# print the JSON string representation of the object
print(ApigenerativevalidationListTestRunsResponse.to_json())

# convert the object into a dict
apigenerativevalidation_list_test_runs_response_dict = apigenerativevalidation_list_test_runs_response_instance.to_dict()
# create an instance of ApigenerativevalidationListTestRunsResponse from a dict
apigenerativevalidation_list_test_runs_response_from_dict = ApigenerativevalidationListTestRunsResponse.from_dict(apigenerativevalidation_list_test_runs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

