# RimeCreateImageRequest

Request and response for a CreateImage RPC.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the Managed Image. | 
**pip_requirements** | [**List[ManagedImagePipRequirement]**](ManagedImagePipRequirement.md) | List of &#x60;pip&#x60; requirements that specify the customization used for this Image. | 
**package_requirements** | [**List[ManagedImagePackageRequirement]**](ManagedImagePackageRequirement.md) | List of system requirements that specify the customization used for this Image. | [optional] 
**python_version** | **str** | The version of the Python interpreter to use. | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_image_request import RimeCreateImageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateImageRequest from a JSON string
rime_create_image_request_instance = RimeCreateImageRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateImageRequest.to_json())

# convert the object into a dict
rime_create_image_request_dict = rime_create_image_request_instance.to_dict()
# create an instance of RimeCreateImageRequest from a dict
rime_create_image_request_from_dict = RimeCreateImageRequest.from_dict(rime_create_image_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

