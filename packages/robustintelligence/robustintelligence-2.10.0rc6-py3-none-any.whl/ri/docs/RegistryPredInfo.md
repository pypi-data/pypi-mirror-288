# RegistryPredInfo

PredInfo specifies the information needed for a prediction set.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_info** | [**RegistryConnectionInfo**](RegistryConnectionInfo.md) |  | [optional] 
**pred_params** | [**RegistryPredictionParams**](RegistryPredictionParams.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.registry_pred_info import RegistryPredInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryPredInfo from a JSON string
registry_pred_info_instance = RegistryPredInfo.from_json(json)
# print the JSON string representation of the object
print(RegistryPredInfo.to_json())

# convert the object into a dict
registry_pred_info_dict = registry_pred_info_instance.to_dict()
# create an instance of RegistryPredInfo from a dict
registry_pred_info_from_dict = RegistryPredInfo.from_dict(registry_pred_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

