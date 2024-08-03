# RuntimeinfoCustomImageType

CustomImageType is a union of all possible custom managed image and RI managed image.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_image** | [**RuntimeinfoCustomImage**](RuntimeinfoCustomImage.md) |  | [optional] 
**managed_image_name** | **str** | Name of the RI managed image. | [optional] 

## Example

```python
from ri.apiclient.models.runtimeinfo_custom_image_type import RuntimeinfoCustomImageType

# TODO update the JSON string below
json = "{}"
# create an instance of RuntimeinfoCustomImageType from a JSON string
runtimeinfo_custom_image_type_instance = RuntimeinfoCustomImageType.from_json(json)
# print the JSON string representation of the object
print(RuntimeinfoCustomImageType.to_json())

# convert the object into a dict
runtimeinfo_custom_image_type_dict = runtimeinfo_custom_image_type_instance.to_dict()
# create an instance of RuntimeinfoCustomImageType from a dict
runtimeinfo_custom_image_type_from_dict = RuntimeinfoCustomImageType.from_dict(runtimeinfo_custom_image_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

