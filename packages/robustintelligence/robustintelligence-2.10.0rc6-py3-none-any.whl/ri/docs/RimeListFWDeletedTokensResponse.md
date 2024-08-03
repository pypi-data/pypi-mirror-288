# RimeListFWDeletedTokensResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token_hashes** | **List[str]** |  | [optional] 
**next_page_token** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_fw_deleted_tokens_response import RimeListFWDeletedTokensResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListFWDeletedTokensResponse from a JSON string
rime_list_fw_deleted_tokens_response_instance = RimeListFWDeletedTokensResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListFWDeletedTokensResponse.to_json())

# convert the object into a dict
rime_list_fw_deleted_tokens_response_dict = rime_list_fw_deleted_tokens_response_instance.to_dict()
# create an instance of RimeListFWDeletedTokensResponse from a dict
rime_list_fw_deleted_tokens_response_from_dict = RimeListFWDeletedTokensResponse.from_dict(rime_list_fw_deleted_tokens_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

