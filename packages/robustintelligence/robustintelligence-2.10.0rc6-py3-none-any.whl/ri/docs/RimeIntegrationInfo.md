# RimeIntegrationInfo

Represents an Integration and its configuration status.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**integration** | [**RischemaintegrationIntegration**](RischemaintegrationIntegration.md) |  | [optional] 
**configured** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_integration_info import RimeIntegrationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RimeIntegrationInfo from a JSON string
rime_integration_info_instance = RimeIntegrationInfo.from_json(json)
# print the JSON string representation of the object
print(RimeIntegrationInfo.to_json())

# convert the object into a dict
rime_integration_info_dict = rime_integration_info_instance.to_dict()
# create an instance of RimeIntegrationInfo from a dict
rime_integration_info_from_dict = RimeIntegrationInfo.from_dict(rime_integration_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

