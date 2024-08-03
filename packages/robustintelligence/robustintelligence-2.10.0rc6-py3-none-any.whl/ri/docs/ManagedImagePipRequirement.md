# ManagedImagePipRequirement


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the library. | [optional] 
**version_specifier** | **str** | Specifier for a version of the library, see: https://www.python.org/dev/peps/pep-0440/#version-specifiers or https://peps.python.org/pep-0440/ for reference. | [optional] 

## Example

```python
from ri.apiclient.models.managed_image_pip_requirement import ManagedImagePipRequirement

# TODO update the JSON string below
json = "{}"
# create an instance of ManagedImagePipRequirement from a JSON string
managed_image_pip_requirement_instance = ManagedImagePipRequirement.from_json(json)
# print the JSON string representation of the object
print(ManagedImagePipRequirement.to_json())

# convert the object into a dict
managed_image_pip_requirement_dict = managed_image_pip_requirement_instance.to_dict()
# create an instance of ManagedImagePipRequirement from a dict
managed_image_pip_requirement_from_dict = ManagedImagePipRequirement.from_dict(managed_image_pip_requirement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

