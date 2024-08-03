# RegistryModelPathInfo

Represents info for a file at path that interfaces with a model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** | The path to the model.  This can be a local path or a path to a file in a configured integration. | 

## Example

```python
from ri.apiclient.models.registry_model_path_info import RegistryModelPathInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryModelPathInfo from a JSON string
registry_model_path_info_instance = RegistryModelPathInfo.from_json(json)
# print the JSON string representation of the object
print(RegistryModelPathInfo.to_json())

# convert the object into a dict
registry_model_path_info_dict = registry_model_path_info_instance.to_dict()
# create an instance of RegistryModelPathInfo from a dict
registry_model_path_info_from_dict = RegistryModelPathInfo.from_dict(registry_model_path_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

