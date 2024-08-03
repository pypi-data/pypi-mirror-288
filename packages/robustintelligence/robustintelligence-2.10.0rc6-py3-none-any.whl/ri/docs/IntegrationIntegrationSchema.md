# IntegrationIntegrationSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**variables** | [**List[SchemaintegrationIntegrationVariable]**](SchemaintegrationIntegrationVariable.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.integration_integration_schema import IntegrationIntegrationSchema

# TODO update the JSON string below
json = "{}"
# create an instance of IntegrationIntegrationSchema from a JSON string
integration_integration_schema_instance = IntegrationIntegrationSchema.from_json(json)
# print the JSON string representation of the object
print(IntegrationIntegrationSchema.to_json())

# convert the object into a dict
integration_integration_schema_dict = integration_integration_schema_instance.to_dict()
# create an instance of IntegrationIntegrationSchema from a dict
integration_integration_schema_from_dict = IntegrationIntegrationSchema.from_dict(integration_integration_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

