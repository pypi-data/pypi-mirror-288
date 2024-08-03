# RegistryHuggingFaceDataInfo

HuggingFaceDataInfo provides the information needed to load a HuggingFace dataset.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_uri** | **str** | The unique identifier of the dataset. | 
**split_name** | **str** | The string that represents the name of a predefined subset of data. | 
**loading_params_json** | **str** | This is a JSON-serialized string from a map. | [optional] 

## Example

```python
from ri.apiclient.models.registry_hugging_face_data_info import RegistryHuggingFaceDataInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryHuggingFaceDataInfo from a JSON string
registry_hugging_face_data_info_instance = RegistryHuggingFaceDataInfo.from_json(json)
# print the JSON string representation of the object
print(RegistryHuggingFaceDataInfo.to_json())

# convert the object into a dict
registry_hugging_face_data_info_dict = registry_hugging_face_data_info_instance.to_dict()
# create an instance of RegistryHuggingFaceDataInfo from a dict
registry_hugging_face_data_info_from_dict = RegistryHuggingFaceDataInfo.from_dict(registry_hugging_face_data_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

