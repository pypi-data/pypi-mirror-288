# SchemaintegrationIntegrationVariable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**sensitivity** | [**IntegrationVariableSensitivity**](IntegrationVariableSensitivity.md) |  | [optional] 
**value** | **str** | Field \&quot;value\&quot; is plaintext if the variable is not sensitive or nil if it is secret. | [optional] 

## Example

```python
from ri.apiclient.models.schemaintegration_integration_variable import SchemaintegrationIntegrationVariable

# TODO update the JSON string below
json = "{}"
# create an instance of SchemaintegrationIntegrationVariable from a JSON string
schemaintegration_integration_variable_instance = SchemaintegrationIntegrationVariable.from_json(json)
# print the JSON string representation of the object
print(SchemaintegrationIntegrationVariable.to_json())

# convert the object into a dict
schemaintegration_integration_variable_dict = schemaintegration_integration_variable_instance.to_dict()
# create an instance of SchemaintegrationIntegrationVariable from a dict
schemaintegration_integration_variable_from_dict = SchemaintegrationIntegrationVariable.from_dict(schemaintegration_integration_variable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

