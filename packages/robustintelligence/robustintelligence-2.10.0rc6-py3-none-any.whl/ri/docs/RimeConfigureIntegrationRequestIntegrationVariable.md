# RimeConfigureIntegrationRequestIntegrationVariable

Represents a variable for an Integration.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the Integration variable. | [optional] 
**value** | **str** | Value of the Integration variable. | [optional] 

## Example

```python
from ri.apiclient.models.rime_configure_integration_request_integration_variable import RimeConfigureIntegrationRequestIntegrationVariable

# TODO update the JSON string below
json = "{}"
# create an instance of RimeConfigureIntegrationRequestIntegrationVariable from a JSON string
rime_configure_integration_request_integration_variable_instance = RimeConfigureIntegrationRequestIntegrationVariable.from_json(json)
# print the JSON string representation of the object
print(RimeConfigureIntegrationRequestIntegrationVariable.to_json())

# convert the object into a dict
rime_configure_integration_request_integration_variable_dict = rime_configure_integration_request_integration_variable_instance.to_dict()
# create an instance of RimeConfigureIntegrationRequestIntegrationVariable from a dict
rime_configure_integration_request_integration_variable_from_dict = RimeConfigureIntegrationRequestIntegrationVariable.from_dict(rime_configure_integration_request_integration_variable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

