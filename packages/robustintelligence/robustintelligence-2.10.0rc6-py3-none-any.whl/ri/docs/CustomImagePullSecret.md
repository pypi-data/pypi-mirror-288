# CustomImagePullSecret

Description of the secret required to pull a custom image.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the Kubernetes pull secret that stores the required pull secret for the custom image. | [optional] 

## Example

```python
from ri.apiclient.models.custom_image_pull_secret import CustomImagePullSecret

# TODO update the JSON string below
json = "{}"
# create an instance of CustomImagePullSecret from a JSON string
custom_image_pull_secret_instance = CustomImagePullSecret.from_json(json)
# print the JSON string representation of the object
print(CustomImagePullSecret.to_json())

# convert the object into a dict
custom_image_pull_secret_dict = custom_image_pull_secret_instance.to_dict()
# create an instance of CustomImagePullSecret from a dict
custom_image_pull_secret_from_dict = CustomImagePullSecret.from_dict(custom_image_pull_secret_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

