# RimeManagedImage

A representation of a custom Image whose tag or version is managed by the ImageRegistry.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The external name of the image. This name must match the /^[a-z][a-z0-9]*(?:[_-][a-z0-9]+)*$/ regular expression. See the naming rules in https://docs.docker.com/engine/reference/commandline/tag/#extended-description https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html from which the naming convention derives. The above names are valid ECR or Docker image names. | [optional] 
**base_image** | [**RimeImageReference**](RimeImageReference.md) |  | [optional] 
**role_type** | [**ManagedImageRoleType**](ManagedImageRoleType.md) |  | [optional] 
**child_images** | [**List[RimeImageReference]**](RimeImageReference.md) | The set of images that use this image as a source. | [optional] 
**rime_tag** | **str** | The tag of the RIME wheel used to build the managed image. | [optional] 
**repo_uri** | **str** | The URI of the repository. | [optional] 
**status** | [**RimeManagedImageStatus**](RimeManagedImageStatus.md) |  | [optional] 
**package_requirements** | [**List[ManagedImagePackageRequirement]**](ManagedImagePackageRequirement.md) | A list of all system package requirements used to build this image. | [optional] 
**pip_requirements** | [**List[ManagedImagePipRequirement]**](ManagedImagePipRequirement.md) | A list of all pip requirements used to build this image. | [optional] 
**pip_libraries** | [**List[ManagedImagePipLibrary]**](ManagedImagePipLibrary.md) | A list of all pip libraries installed on this image as obtained by running &#x60;pip list&#x60;. | [optional] 
**python_version** | **str** | The version of Python used to build the Robust Intelligence image. | [optional] 

## Example

```python
from ri.apiclient.models.rime_managed_image import RimeManagedImage

# TODO update the JSON string below
json = "{}"
# create an instance of RimeManagedImage from a JSON string
rime_managed_image_instance = RimeManagedImage.from_json(json)
# print the JSON string representation of the object
print(RimeManagedImage.to_json())

# convert the object into a dict
rime_managed_image_dict = rime_managed_image_instance.to_dict()
# create an instance of RimeManagedImage from a dict
rime_managed_image_from_dict = RimeManagedImage.from_dict(rime_managed_image_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

