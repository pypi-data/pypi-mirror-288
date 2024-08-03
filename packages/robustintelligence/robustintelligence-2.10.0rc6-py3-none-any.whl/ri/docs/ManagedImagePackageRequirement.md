# ManagedImagePackageRequirement

A requirement specifying a system package to install on the Image.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the package. | [optional] 
**version_specifier** | **str** |  | [optional] 
**package_type** | [**RimeManagedImagePackageType**](RimeManagedImagePackageType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.managed_image_package_requirement import ManagedImagePackageRequirement

# TODO update the JSON string below
json = "{}"
# create an instance of ManagedImagePackageRequirement from a JSON string
managed_image_package_requirement_instance = ManagedImagePackageRequirement.from_json(json)
# print the JSON string representation of the object
print(ManagedImagePackageRequirement.to_json())

# convert the object into a dict
managed_image_package_requirement_dict = managed_image_package_requirement_instance.to_dict()
# create an instance of ManagedImagePackageRequirement from a dict
managed_image_package_requirement_from_dict = ManagedImagePackageRequirement.from_dict(managed_image_package_requirement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

