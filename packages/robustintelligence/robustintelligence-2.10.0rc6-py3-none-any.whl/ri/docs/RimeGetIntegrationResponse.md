# RimeGetIntegrationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**integration_info** | [**RimeIntegrationInfo**](RimeIntegrationInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_integration_response import RimeGetIntegrationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetIntegrationResponse from a JSON string
rime_get_integration_response_instance = RimeGetIntegrationResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetIntegrationResponse.to_json())

# convert the object into a dict
rime_get_integration_response_dict = rime_get_integration_response_instance.to_dict()
# create an instance of RimeGetIntegrationResponse from a dict
rime_get_integration_response_from_dict = RimeGetIntegrationResponse.from_dict(rime_get_integration_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

