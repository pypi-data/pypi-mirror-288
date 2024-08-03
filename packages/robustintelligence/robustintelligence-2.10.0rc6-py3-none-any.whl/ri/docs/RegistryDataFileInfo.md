# RegistryDataFileInfo

DataFileInfo specifies how to connect to a data file.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** | The path to the data file. | 
**data_type** | [**RegistryDataType**](RegistryDataType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.registry_data_file_info import RegistryDataFileInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryDataFileInfo from a JSON string
registry_data_file_info_instance = RegistryDataFileInfo.from_json(json)
# print the JSON string representation of the object
print(RegistryDataFileInfo.to_json())

# convert the object into a dict
registry_data_file_info_dict = registry_data_file_info_instance.to_dict()
# create an instance of RegistryDataFileInfo from a dict
registry_data_file_info_from_dict = RegistryDataFileInfo.from_dict(registry_data_file_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

