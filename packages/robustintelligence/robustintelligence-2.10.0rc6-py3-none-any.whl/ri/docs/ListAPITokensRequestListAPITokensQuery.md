# ListAPITokensRequestListAPITokensQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token_type** | [**RimeTokenType**](RimeTokenType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.list_api_tokens_request_list_api_tokens_query import ListAPITokensRequestListAPITokensQuery

# TODO update the JSON string below
json = "{}"
# create an instance of ListAPITokensRequestListAPITokensQuery from a JSON string
list_api_tokens_request_list_api_tokens_query_instance = ListAPITokensRequestListAPITokensQuery.from_json(json)
# print the JSON string representation of the object
print(ListAPITokensRequestListAPITokensQuery.to_json())

# convert the object into a dict
list_api_tokens_request_list_api_tokens_query_dict = list_api_tokens_request_list_api_tokens_query_instance.to_dict()
# create an instance of ListAPITokensRequestListAPITokensQuery from a dict
list_api_tokens_request_list_api_tokens_query_from_dict = ListAPITokensRequestListAPITokensQuery.from_dict(list_api_tokens_request_list_api_tokens_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

