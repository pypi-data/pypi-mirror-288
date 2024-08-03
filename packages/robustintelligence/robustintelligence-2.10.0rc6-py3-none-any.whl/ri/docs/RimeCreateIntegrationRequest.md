# RimeCreateIntegrationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**integration** | [**RischemaintegrationIntegration**](RischemaintegrationIntegration.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_integration_request import RimeCreateIntegrationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateIntegrationRequest from a JSON string
rime_create_integration_request_instance = RimeCreateIntegrationRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateIntegrationRequest.to_json())

# convert the object into a dict
rime_create_integration_request_dict = rime_create_integration_request_instance.to_dict()
# create an instance of RimeCreateIntegrationRequest from a dict
rime_create_integration_request_from_dict = RimeCreateIntegrationRequest.from_dict(rime_create_integration_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

