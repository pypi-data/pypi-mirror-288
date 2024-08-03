# RimeCreateIntegrationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**integration_info** | [**RimeIntegrationInfo**](RimeIntegrationInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_integration_response import RimeCreateIntegrationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateIntegrationResponse from a JSON string
rime_create_integration_response_instance = RimeCreateIntegrationResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateIntegrationResponse.to_json())

# convert the object into a dict
rime_create_integration_response_dict = rime_create_integration_response_instance.to_dict()
# create an instance of RimeCreateIntegrationResponse from a dict
rime_create_integration_response_from_dict = RimeCreateIntegrationResponse.from_dict(rime_create_integration_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

