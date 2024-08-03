# RimeListAPITokensResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_token_infos** | [**List[RimeAPITokenInfo]**](RimeAPITokenInfo.md) |  | [optional] 
**next_page_token** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_api_tokens_response import RimeListAPITokensResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListAPITokensResponse from a JSON string
rime_list_api_tokens_response_instance = RimeListAPITokensResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListAPITokensResponse.to_json())

# convert the object into a dict
rime_list_api_tokens_response_dict = rime_list_api_tokens_response_instance.to_dict()
# create an instance of RimeListAPITokensResponse from a dict
rime_list_api_tokens_response_from_dict = RimeListAPITokensResponse.from_dict(rime_list_api_tokens_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

