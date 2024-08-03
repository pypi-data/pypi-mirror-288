# RegistryModelInfo

Represents the information of the model to test.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_path** | [**RegistryModelPathInfo**](RegistryModelPathInfo.md) |  | [optional] 
**hugging_face** | [**RegistryHuggingFaceModelInfo**](RegistryHuggingFaceModelInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.registry_model_info import RegistryModelInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryModelInfo from a JSON string
registry_model_info_instance = RegistryModelInfo.from_json(json)
# print the JSON string representation of the object
print(RegistryModelInfo.to_json())

# convert the object into a dict
registry_model_info_dict = registry_model_info_instance.to_dict()
# create an instance of RegistryModelInfo from a dict
registry_model_info_from_dict = RegistryModelInfo.from_dict(registry_model_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

