# RegistryDataCollectorInfo

DataCollectorInfo provides the information needed to load a data stream from a data collector.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_stream_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.registry_data_collector_info import RegistryDataCollectorInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryDataCollectorInfo from a JSON string
registry_data_collector_info_instance = RegistryDataCollectorInfo.from_json(json)
# print the JSON string representation of the object
print(RegistryDataCollectorInfo.to_json())

# convert the object into a dict
registry_data_collector_info_dict = registry_data_collector_info_instance.to_dict()
# create an instance of RegistryDataCollectorInfo from a dict
registry_data_collector_info_from_dict = RegistryDataCollectorInfo.from_dict(registry_data_collector_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

