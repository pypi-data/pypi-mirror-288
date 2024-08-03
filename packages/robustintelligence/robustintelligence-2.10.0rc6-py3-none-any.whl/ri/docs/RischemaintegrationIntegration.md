# RischemaintegrationIntegration

Integration object in RIME.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**creation_time** | **datetime** |  | [optional] 
**name** | **str** |  | [optional] 
**type** | [**IntegrationIntegrationType**](IntegrationIntegrationType.md) |  | [optional] 
**var_schema** | [**IntegrationIntegrationSchema**](IntegrationIntegrationSchema.md) |  | [optional] 
**level** | [**IntegrationIntegrationLevel**](IntegrationIntegrationLevel.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rischemaintegration_integration import RischemaintegrationIntegration

# TODO update the JSON string below
json = "{}"
# create an instance of RischemaintegrationIntegration from a JSON string
rischemaintegration_integration_instance = RischemaintegrationIntegration.from_json(json)
# print the JSON string representation of the object
print(RischemaintegrationIntegration.to_json())

# convert the object into a dict
rischemaintegration_integration_dict = rischemaintegration_integration_instance.to_dict()
# create an instance of RischemaintegrationIntegration from a dict
rischemaintegration_integration_from_dict = RischemaintegrationIntegration.from_dict(rischemaintegration_integration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

