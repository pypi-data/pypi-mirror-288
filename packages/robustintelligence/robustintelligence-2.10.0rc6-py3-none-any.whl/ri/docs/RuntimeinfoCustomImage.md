# RuntimeinfoCustomImage

CustomImage is an external image provided by the customer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the custom image (e.g. a docker image name). | [optional] 
**pull_secret** | [**CustomImagePullSecret**](CustomImagePullSecret.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.runtimeinfo_custom_image import RuntimeinfoCustomImage

# TODO update the JSON string below
json = "{}"
# create an instance of RuntimeinfoCustomImage from a JSON string
runtimeinfo_custom_image_instance = RuntimeinfoCustomImage.from_json(json)
# print the JSON string representation of the object
print(RuntimeinfoCustomImage.to_json())

# convert the object into a dict
runtimeinfo_custom_image_dict = runtimeinfo_custom_image_instance.to_dict()
# create an instance of RuntimeinfoCustomImage from a dict
runtimeinfo_custom_image_from_dict = RuntimeinfoCustomImage.from_dict(runtimeinfo_custom_image_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

