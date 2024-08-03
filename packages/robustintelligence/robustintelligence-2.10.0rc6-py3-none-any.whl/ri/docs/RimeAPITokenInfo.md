# RimeAPITokenInfo

API token object.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**name** | **str** | The name of the API token. | [optional] 
**suffix** | **str** | The suffix of the API token, which is visible in the Robust Intelligence web application. | [optional] 
**creation_time** | **datetime** |  | [optional] 
**expiration_time** | **datetime** |  | [optional] 
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**user_id** | **str** | The ID of the user who created the API token. | [optional] 
**token_type** | [**RimeTokenType**](RimeTokenType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_api_token_info import RimeAPITokenInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RimeAPITokenInfo from a JSON string
rime_api_token_info_instance = RimeAPITokenInfo.from_json(json)
# print the JSON string representation of the object
print(RimeAPITokenInfo.to_json())

# convert the object into a dict
rime_api_token_info_dict = rime_api_token_info_instance.to_dict()
# create an instance of RimeAPITokenInfo from a dict
rime_api_token_info_from_dict = RimeAPITokenInfo.from_dict(rime_api_token_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

