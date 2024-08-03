# RegistryMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tags** | **List[str]** | Tags are optional single strings used to identify and organize across a project. | [optional] 
**extra_info** | **str** | Metadata are optional json encoded information that users wish to associate. | [optional] 

## Example

```python
from ri.apiclient.models.registry_metadata import RegistryMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryMetadata from a JSON string
registry_metadata_instance = RegistryMetadata.from_json(json)
# print the JSON string representation of the object
print(RegistryMetadata.to_json())

# convert the object into a dict
registry_metadata_dict = registry_metadata_instance.to_dict()
# create an instance of RegistryMetadata from a dict
registry_metadata_from_dict = RegistryMetadata.from_dict(registry_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

