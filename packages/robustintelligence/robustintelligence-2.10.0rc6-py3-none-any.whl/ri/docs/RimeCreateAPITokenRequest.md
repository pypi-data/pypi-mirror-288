# RimeCreateAPITokenRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the API token. | 
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**token_type** | [**RimeTokenType**](RimeTokenType.md) |  | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**expiry_days** | **int** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_api_token_request import RimeCreateAPITokenRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateAPITokenRequest from a JSON string
rime_create_api_token_request_instance = RimeCreateAPITokenRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateAPITokenRequest.to_json())

# convert the object into a dict
rime_create_api_token_request_dict = rime_create_api_token_request_instance.to_dict()
# create an instance of RimeCreateAPITokenRequest from a dict
rime_create_api_token_request_from_dict = RimeCreateAPITokenRequest.from_dict(rime_create_api_token_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

