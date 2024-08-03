# RegistryDataInfo

DataInfo specifies the information needed for a dataset.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_info** | [**RegistryConnectionInfo**](RegistryConnectionInfo.md) |  | [optional] 
**data_params** | [**RegistryDataParams**](RegistryDataParams.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.registry_data_info import RegistryDataInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryDataInfo from a JSON string
registry_data_info_instance = RegistryDataInfo.from_json(json)
# print the JSON string representation of the object
print(RegistryDataInfo.to_json())

# convert the object into a dict
registry_data_info_dict = registry_data_info_instance.to_dict()
# create an instance of RegistryDataInfo from a dict
registry_data_info_from_dict = RegistryDataInfo.from_dict(registry_data_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

