# RegistryConnectionInfo

ConnectionInfo specifies how to connect to a data source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_file** | [**RegistryDataFileInfo**](RegistryDataFileInfo.md) |  | [optional] 
**data_loading** | [**RegistryDataLoadingInfo**](RegistryDataLoadingInfo.md) |  | [optional] 
**data_collector** | [**RegistryDataCollectorInfo**](RegistryDataCollectorInfo.md) |  | [optional] 
**databricks** | [**RegistryDatabricksInfo**](RegistryDatabricksInfo.md) |  | [optional] 
**hugging_face** | [**RegistryHuggingFaceDataInfo**](RegistryHuggingFaceDataInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.registry_connection_info import RegistryConnectionInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryConnectionInfo from a JSON string
registry_connection_info_instance = RegistryConnectionInfo.from_json(json)
# print the JSON string representation of the object
print(RegistryConnectionInfo.to_json())

# convert the object into a dict
registry_connection_info_dict = registry_connection_info_instance.to_dict()
# create an instance of RegistryConnectionInfo from a dict
registry_connection_info_from_dict = RegistryConnectionInfo.from_dict(registry_connection_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

