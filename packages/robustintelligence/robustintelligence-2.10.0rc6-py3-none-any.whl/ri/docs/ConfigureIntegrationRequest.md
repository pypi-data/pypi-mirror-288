# ConfigureIntegrationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**integration_id** | **object** | Unique ID of an object in RIME. | [optional] 
**variables** | [**List[RimeConfigureIntegrationRequestIntegrationVariable]**](RimeConfigureIntegrationRequestIntegrationVariable.md) |  | 

## Example

```python
from ri.apiclient.models.configure_integration_request import ConfigureIntegrationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigureIntegrationRequest from a JSON string
configure_integration_request_instance = ConfigureIntegrationRequest.from_json(json)
# print the JSON string representation of the object
print(ConfigureIntegrationRequest.to_json())

# convert the object into a dict
configure_integration_request_dict = configure_integration_request_instance.to_dict()
# create an instance of ConfigureIntegrationRequest from a dict
configure_integration_request_from_dict = ConfigureIntegrationRequest.from_dict(configure_integration_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

