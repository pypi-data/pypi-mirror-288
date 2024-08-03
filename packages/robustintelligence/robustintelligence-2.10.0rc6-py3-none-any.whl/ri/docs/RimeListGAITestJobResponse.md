# RimeListGAITestJobResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**jobs** | [**List[RimeJobMetadata]**](RimeJobMetadata.md) |  | [optional] 
**next_page_token** | **str** | Use this page token in your next ListJobs call to access the next page of results. | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_gai_test_job_response import RimeListGAITestJobResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListGAITestJobResponse from a JSON string
rime_list_gai_test_job_response_instance = RimeListGAITestJobResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListGAITestJobResponse.to_json())

# convert the object into a dict
rime_list_gai_test_job_response_dict = rime_list_gai_test_job_response_instance.to_dict()
# create an instance of RimeListGAITestJobResponse from a dict
rime_list_gai_test_job_response_from_dict = RimeListGAITestJobResponse.from_dict(rime_list_gai_test_job_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

