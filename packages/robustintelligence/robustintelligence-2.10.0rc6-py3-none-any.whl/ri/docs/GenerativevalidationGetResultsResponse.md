# GenerativevalidationGetResultsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[GenerativevalidationGenerativeTestingResult]**](GenerativevalidationGenerativeTestingResult.md) | The list of generative testing results. | [optional] 
**next_page_token** | **str** | A token representing the next page from the list returned by a query. | [optional] 
**has_more** | **bool** | A Boolean flag that specifies whether there are more results to return. | [optional] 
**job_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**job_status** | [**RimeJobStatus**](RimeJobStatus.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.generativevalidation_get_results_response import GenerativevalidationGetResultsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativevalidationGetResultsResponse from a JSON string
generativevalidation_get_results_response_instance = GenerativevalidationGetResultsResponse.from_json(json)
# print the JSON string representation of the object
print(GenerativevalidationGetResultsResponse.to_json())

# convert the object into a dict
generativevalidation_get_results_response_dict = generativevalidation_get_results_response_instance.to_dict()
# create an instance of GenerativevalidationGetResultsResponse from a dict
generativevalidation_get_results_response_from_dict = GenerativevalidationGetResultsResponse.from_dict(generativevalidation_get_results_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

