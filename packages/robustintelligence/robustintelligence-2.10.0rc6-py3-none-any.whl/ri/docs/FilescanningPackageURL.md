# FilescanningPackageURL

A Package URL (PURL) is a uniform way to identify a software package. A PURL has seven components: scheme:type/namespace/name@version?qualifiers#subpath The scheme is always pkg. See: https://github.com/package-url/PURL-spec for more details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**SchemafilescanningPackageType**](SchemafilescanningPackageType.md) |  | [optional] 
**namespace** | **str** | Optional. The name prefix such as a GitHub user or organization, Maven groupid, or a Docker image owner. | [optional] 
**name** | **str** | The name of the package. | [optional] 
**version** | **str** | Optional. The version of the package. | [optional] 
**qualifiers** | **Dict[str, str]** | Optional. Additional qualifying data for a package such as an OS, architecture, a distro, etc. | [optional] 
**subpath** | **str** | Optional. A subpath within a package, relative to the package root. | [optional] 

## Example

```python
from ri.apiclient.models.filescanning_package_url import FilescanningPackageURL

# TODO update the JSON string below
json = "{}"
# create an instance of FilescanningPackageURL from a JSON string
filescanning_package_url_instance = FilescanningPackageURL.from_json(json)
# print the JSON string representation of the object
print(FilescanningPackageURL.to_json())

# convert the object into a dict
filescanning_package_url_dict = filescanning_package_url_instance.to_dict()
# create an instance of FilescanningPackageURL from a dict
filescanning_package_url_from_dict = FilescanningPackageURL.from_dict(filescanning_package_url_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

