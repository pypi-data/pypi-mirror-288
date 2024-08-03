# ManagedImagePipLibrary

A pip library to install on the Managed Image.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the library. | [optional] 
**version** | **str** | Version of the library. | [optional] 

## Example

```python
from ri.apiclient.models.managed_image_pip_library import ManagedImagePipLibrary

# TODO update the JSON string below
json = "{}"
# create an instance of ManagedImagePipLibrary from a JSON string
managed_image_pip_library_instance = ManagedImagePipLibrary.from_json(json)
# print the JSON string representation of the object
print(ManagedImagePipLibrary.to_json())

# convert the object into a dict
managed_image_pip_library_dict = managed_image_pip_library_instance.to_dict()
# create an instance of ManagedImagePipLibrary from a dict
managed_image_pip_library_from_dict = ManagedImagePipLibrary.from_dict(managed_image_pip_library_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

