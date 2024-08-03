# RimeCreateAPITokenResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**full_api_token** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_api_token_response import RimeCreateAPITokenResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateAPITokenResponse from a JSON string
rime_create_api_token_response_instance = RimeCreateAPITokenResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateAPITokenResponse.to_json())

# convert the object into a dict
rime_create_api_token_response_dict = rime_create_api_token_response_instance.to_dict()
# create an instance of RimeCreateAPITokenResponse from a dict
rime_create_api_token_response_from_dict = RimeCreateAPITokenResponse.from_dict(rime_create_api_token_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

