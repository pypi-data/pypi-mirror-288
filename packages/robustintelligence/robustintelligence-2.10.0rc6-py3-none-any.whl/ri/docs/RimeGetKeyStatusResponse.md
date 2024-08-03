# RimeGetKeyStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**CustomermanagedkeyKeyStatus**](CustomermanagedkeyKeyStatus.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_key_status_response import RimeGetKeyStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetKeyStatusResponse from a JSON string
rime_get_key_status_response_instance = RimeGetKeyStatusResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetKeyStatusResponse.to_json())

# convert the object into a dict
rime_get_key_status_response_dict = rime_get_key_status_response_instance.to_dict()
# create an instance of RimeGetKeyStatusResponse from a dict
rime_get_key_status_response_from_dict = RimeGetKeyStatusResponse.from_dict(rime_get_key_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

