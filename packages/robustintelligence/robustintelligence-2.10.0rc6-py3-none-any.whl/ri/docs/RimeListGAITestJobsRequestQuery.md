# RimeListGAITestJobsRequestQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selected_statuses** | [**List[RimeJobStatus]**](RimeJobStatus.md) | Specifies a set of statuses. The query only returns results with a status in the specified set. Specify no statuses to return all results. | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_gai_test_jobs_request_query import RimeListGAITestJobsRequestQuery

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListGAITestJobsRequestQuery from a JSON string
rime_list_gai_test_jobs_request_query_instance = RimeListGAITestJobsRequestQuery.from_json(json)
# print the JSON string representation of the object
print(RimeListGAITestJobsRequestQuery.to_json())

# convert the object into a dict
rime_list_gai_test_jobs_request_query_dict = rime_list_gai_test_jobs_request_query_instance.to_dict()
# create an instance of RimeListGAITestJobsRequestQuery from a dict
rime_list_gai_test_jobs_request_query_from_dict = RimeListGAITestJobsRequestQuery.from_dict(rime_list_gai_test_jobs_request_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

