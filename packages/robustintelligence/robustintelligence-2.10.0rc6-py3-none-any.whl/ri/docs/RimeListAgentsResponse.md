# RimeListAgentsResponse

ListAgentsResponse returns the list of agent metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agents** | [**List[RimeAgent]**](RimeAgent.md) |  | [optional] 
**next_page_token** | **str** | Use this page token in your next ListAgents call to access to the next page of results. | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_agents_response import RimeListAgentsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListAgentsResponse from a JSON string
rime_list_agents_response_instance = RimeListAgentsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListAgentsResponse.to_json())

# convert the object into a dict
rime_list_agents_response_dict = rime_list_agents_response_instance.to_dict()
# create an instance of RimeListAgentsResponse from a dict
rime_list_agents_response_from_dict = RimeListAgentsResponse.from_dict(rime_list_agents_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

